from __future__ import annotations

import datetime as dt

from celery import shared_task
from django.utils import timezone

from market.db import models
from .llm import analyzer
from .news import service
from .signals import generator
from .trading import executor
from .ml import patterns
from .utils.config import get_config_value


@shared_task
def poll_news_providers() -> int:
    interval = get_config_value("NEWS_POLL_SECONDS", 180)
    since = timezone.now() - dt.timedelta(seconds=interval)
    return service.poll_all_providers(since)


@shared_task
def analyze_new_articles_llm() -> int:
    articles = models.Article.objects.filter(sentiments__isnull=True)[:10]
    sentiments = analyzer.analyze_articles(articles)
    generator.generate_signals_from_sentiments(sentiments)
    return len(sentiments)


@shared_task
def generate_fallback_market_driver_if_quiet() -> int:
    signal = generator.generate_fallback_signal()
    return 1 if signal else 0


@shared_task
def evaluate_signals_and_trade() -> int:
    active_signals = models.Signal.objects.filter(expires_at__gt=timezone.now())
    count = 0
    for signal in active_signals:
        if not signal.orders.exists():
            executor.execute_signal(signal)
            count += 1
    return count


@shared_task
def monitor_positions_for_tp_sl() -> int:
    closed = 0
    for position in models.Position.objects.filter(closed_at__isnull=True):
        # TODO: implement real PnL monitoring using Alpaca quotes
        position.closed_at = timezone.now()
        position.pnl_pct = 10
        position.save(update_fields=["closed_at", "pnl_pct"])
        closed += 1
    return closed


@shared_task
def train_ml_models_daily() -> int:
    snapshots = patterns.evaluate_latest_patterns()
    return len(snapshots)


@shared_task
def run_backtest_job(params: dict) -> dict:
    from .scripts import backtest_runner

    return backtest_runner.run_backtest(params)
