from __future__ import annotations

import datetime as dt

from django.utils import dateparse
from django.utils import timezone

from market.db import models


def save_articles_from_webhook(provider: str, payloads: list[dict]) -> int:
    created = 0
    for payload in payloads:
        url = payload.get("url")
        if not url:
            continue
        defaults = {
            "source": payload.get("source", provider),
            "published_at": dateparse.parse_datetime(payload.get("published_at")) or timezone.now(),
            "title": payload.get("title", ""),
            "body": payload.get("body", ""),
            "tickers": payload.get("tickers", []),
            "raw_json": payload,
        }
        obj, created_flag = models.Article.objects.get_or_create(url=url, defaults=defaults)
        if created_flag:
            created += 1
    return created
