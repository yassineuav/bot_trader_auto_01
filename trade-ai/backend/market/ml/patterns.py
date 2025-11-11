from __future__ import annotations

import datetime as dt
import io
import logging
from dataclasses import dataclass
from typing import Iterable, List

import numpy as np
import pandas as pd
import pandas_ta as ta
from django.utils import timezone
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from market.db import models
from ..utils.config import get_config_value

logger = logging.getLogger(__name__)


@dataclass
class PatternResult:
    symbol: str
    verdict: str
    confidence_pct: int


def _load_price_history(symbol: str, days: int = 60) -> pd.DataFrame:
    # TODO: integrate with market data provider
    rng = pd.date_range(end=timezone.now(), periods=days, freq="B")
    prices = np.linspace(400, 420, len(rng)) + np.random.normal(0, 2, len(rng))
    df = pd.DataFrame({
        "open": prices,
        "high": prices + np.random.uniform(0, 2, len(rng)),
        "low": prices - np.random.uniform(0, 2, len(rng)),
        "close": prices + np.random.normal(0, 1, len(rng)),
        "volume": np.random.randint(1_000_000, 3_000_000, len(rng)),
    }, index=rng)
    return df


def _feature_engineer(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["return"] = df["close"].pct_change().fillna(0)
    df.ta.rsi(length=14, append=True)
    macd = ta.macd(df["close"], fast=12, slow=26, signal=9)
    df = df.join(macd)
    for window in (9, 20, 50):
        df[f"ma_{window}"] = df["close"].rolling(window).mean().fillna(method="bfill")
    df["volatility"] = df["return"].rolling(5).std().fillna(0)
    df.dropna(inplace=True)
    return df


def _train_model(X: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model


def evaluate_latest_patterns(symbols: Iterable[str] | None = None) -> List[models.PatternSnapshot]:
    if symbols is None:
        symbols = get_config_value("PRIMARY_SYMBOLS", ["SPY", "IWM"])
    snapshots: List[models.PatternSnapshot] = []
    for symbol in symbols:
        df = _load_price_history(symbol)
        feats = _feature_engineer(df)
        feats["label"] = (feats["return"].shift(-1) > 0).astype(int)
        feats.dropna(inplace=True)
        if len(feats) < 30:
            continue
        X = feats.drop(columns=["label"])
        y = feats["label"]
        model = _train_model(X, y)
        latest = X.iloc[-1]
        proba = model.predict_proba([latest])[0]
        up_prob = float(proba[1])
        verdict = "call" if up_prob >= 0.6 else "put" if up_prob <= 0.4 else "none"
        confidence_pct = int(abs(up_prob - 0.5) * 200)
        snapshot = models.PatternSnapshot.objects.create(
            symbol=symbol,
            features_json=latest.to_dict(),
            verdict=verdict,
            confidence_pct=confidence_pct,
        )
        snapshots.append(snapshot)
    return snapshots
