from __future__ import annotations

import datetime as dt

import pytest
from django.utils import timezone

from market.db import models


@pytest.mark.django_db
def test_article_creation():
    article = models.Article.objects.create(
        source="Test",
        url="https://example.com/1",
        published_at=timezone.now(),
        title="Headline",
        body="Body",
        tickers=["SPY"],
        raw_json={},
    )
    assert article.pk is not None
