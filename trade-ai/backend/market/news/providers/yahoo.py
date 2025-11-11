from __future__ import annotations

import datetime as dt
import logging
from typing import List

import requests

from .base import NewsProvider, registry

logger = logging.getLogger(__name__)


class YahooNewsProvider(NewsProvider):
    name = "yahoo"
    ENDPOINT = "https://yh-finance.p.rapidapi.com/news/v2/list"

    def __init__(self, api_key: str | None) -> None:
        self.api_key = api_key

    def fetch_since(self, since: dt.datetime) -> List[dict]:
        if not self.api_key:
            logger.warning("Yahoo provider disabled: missing API key")
            return []
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "yh-finance.p.rapidapi.com",
        }
        params = {
            "region": "US",
        }
        response = requests.get(self.ENDPOINT, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        items = data.get("data", {}).get("main", {}).get("stream", [])
        articles: List[dict] = []
        for item in items:
            content = item.get("content", {})
            publish_time = dt.datetime.fromtimestamp(content.get("pubDate", 0), tz=dt.timezone.utc)
            if publish_time < since:
                continue
            articles.append(
                {
                    "source": content.get("provider", {}).get("displayName", "Yahoo"),
                    "url": content.get("canonicalUrl", {}).get("url", ""),
                    "published_at": publish_time.isoformat(),
                    "title": content.get("title", ""),
                    "body": content.get("summary", ""),
                    "tickers": [c.get("symbol") for c in content.get("tickers", []) if c.get("symbol")],
                    "raw": content,
                }
            )
        return articles


def register(api_key: str | None) -> None:
    registry.register(YahooNewsProvider(api_key))
