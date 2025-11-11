from __future__ import annotations

from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Config

DEFAULT_CONFIGS = {
    "ACCOUNT_RISK_PCT": {"value": 0.10},
    "TP_PCT": {"value": 0.50},
    "SL_PCT": {"value": 0.10},
    "NEWS_POLL_SECONDS": {"value": 180},
    "NO_NEWS_LOOKBACK_MIN": {"value": 60},
    "TREND_BULLISH_THRESHOLD": {"value": 0.10},
    "TREND_BEARISH_THRESHOLD": {"value": 0.10},
    "PRIMARY_SYMBOLS": {"value": ["SPY", "IWM"]},
}


@receiver(post_migrate)
def ensure_default_configs(sender, **kwargs):  # pragma: no cover
    if sender.label != "db":
        return
    for key, value in DEFAULT_CONFIGS.items():
        Config.objects.get_or_create(key=key, defaults={"value_json": value})
