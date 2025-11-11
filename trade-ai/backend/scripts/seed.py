from __future__ import annotations

import datetime as dt

from django.utils import timezone

from market.db import models


def run() -> None:
    article, _ = models.Article.objects.get_or_create(
        url="https://example.com/news",
        defaults={
            "source": "Example",
            "published_at": timezone.now() - dt.timedelta(minutes=5),
            "title": "Sample headline",
            "body": "Stocks rally as investors digest economic data.",
            "tickers": ["SPY"],
            "raw_json": {},
        },
    )
    models.Sentiment.objects.get_or_create(
        article=article,
        defaults={
            "pos_pct": 60,
            "neg_pct": 10,
            "label": "positive",
            "llm_version": "seed",
            "trend_bull_bear": "bullish",
            "trend_strength_pct": 20,
            "crowd_reaction_text": "Options flow likely tilts to calls; dip buyers add risk.",
        },
    )


if __name__ == "__main__":
    run()
