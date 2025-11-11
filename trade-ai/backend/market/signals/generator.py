from __future__ import annotations

import datetime as dt
from typing import Iterable

from django.utils import timezone

from market.db import models
from ..llm import analyzer
from ..ml import patterns
from ..utils.config import get_config_value


def generate_signals_from_sentiments(sentiments: Iterable[models.Sentiment]) -> list[models.Signal]:
    signals: list[models.Signal] = []
    for sentiment in sentiments:
        direction = sentiment.trend_bull_bear
        strength = sentiment.trend_strength_pct
        if strength < 10 or direction == "neutral":
            continue
        symbol = "SPY"
        expires = timezone.now() + dt.timedelta(minutes=90)
        signal = models.Signal.objects.create(
            source="news",
            symbol=symbol,
            direction="call" if direction == "bullish" else "put",
            confidence_pct=strength,
            reason=f"LLM {direction} strength {strength}%",
            expires_at=expires,
        )
        signals.append(signal)
    return signals


def generate_fallback_signal() -> models.Signal | None:
    quiet_minutes = get_config_value("NO_NEWS_LOOKBACK_MIN", 60)
    since = timezone.now() - dt.timedelta(minutes=quiet_minutes)
    if models.Signal.objects.filter(created_at__gte=since).exists():
        return None
    fallback = analyzer.fallback_market_driver()
    if fallback.direction == "neutral" or fallback.strength_pct < 10:
        return None
    signal = models.Signal.objects.create(
        source="fallback_llm",
        symbol=fallback.market,
        direction="call" if fallback.direction == "bullish" else "put",
        confidence_pct=fallback.strength_pct,
        reason=fallback.primary_driver,
        expires_at=timezone.now() + dt.timedelta(minutes=90),
    )
    return signal


def generate_ml_signals() -> list[models.Signal]:
    snapshots = patterns.evaluate_latest_patterns()
    signals: list[models.Signal] = []
    for snapshot in snapshots:
        if snapshot.verdict == "none":
            continue
        signal = models.Signal.objects.create(
            source="ml",
            symbol=snapshot.symbol,
            direction="call" if snapshot.verdict == "call" else "put",
            confidence_pct=snapshot.confidence_pct,
            reason="ML pattern detector",
            expires_at=timezone.now() + dt.timedelta(minutes=90),
        )
        signals.append(signal)
    return signals
