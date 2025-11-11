from __future__ import annotations

import datetime as dt
import logging
import os
from typing import Iterable

from django.db import IntegrityError
from django.utils import dateparse, timezone

from market.db import models
from .providers import base
from .providers import yahoo

logger = logging.getLogger(__name__)


def init_providers() -> None:
    yf_cfg = models.Config.objects.filter(key="YF_RAPIDAPI_KEY").first()
    yf_key = yf_cfg.value_json.get("value") if yf_cfg else os.environ.get("YF_RAPIDAPI_KEY")
    yahoo.register(yf_key)
    # TODO: register Benzinga/Reuters providers when API keys are supplied.


def poll_all_providers(since: dt.datetime | None = None) -> int:
    if since is None:
        since = timezone.now() - dt.timedelta(minutes=10)
    if not base.registry.list():
        init_providers()
    total_created = 0
    for provider in base.registry.list():
        articles = provider.fetch_since(since)
        for article in articles:
            try:
                models.Article.objects.create(
                    source=article.get("source", provider.name),
                    url=article["url"],
                    published_at=dateparse.parse_datetime(str(article.get("published_at"))) or timezone.now(),
                    title=article.get("title", ""),
                    body=article.get("body", ""),
                    tickers=article.get("tickers", []),
                    raw_json=article,
                )
                total_created += 1
            except IntegrityError:
                logger.debug("Duplicate article skipped: %s", article.get("url"))
    logger.info("Created %s articles", total_created)
    return total_created
