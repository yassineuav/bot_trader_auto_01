from __future__ import annotations

from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Article(TimestampedModel):
    source = models.CharField(max_length=128)
    url = models.URLField(unique=True)
    published_at = models.DateTimeField()
    title = models.CharField(max_length=512)
    body = models.TextField()
    tickers = models.JSONField(default=list)
    raw_json = models.JSONField(default=dict)

    class Meta:
        ordering = ["-published_at"]


class Sentiment(TimestampedModel):
    article = models.ForeignKey(Article, related_name="sentiments", on_delete=models.CASCADE)
    pos_pct = models.IntegerField()
    neg_pct = models.IntegerField()
    label = models.CharField(max_length=16)
    llm_version = models.CharField(max_length=64)
    trend_bull_bear = models.CharField(max_length=16)
    trend_strength_pct = models.IntegerField()
    crowd_reaction_text = models.TextField()


class Signal(TimestampedModel):
    SOURCE_CHOICES = [
        ("news", "News"),
        ("ml", "Machine Learning"),
        ("fallback_llm", "Fallback LLM"),
    ]
    DIRECTION_CHOICES = [("call", "Call"), ("put", "Put")]

    source = models.CharField(max_length=32, choices=SOURCE_CHOICES)
    symbol = models.CharField(max_length=16)
    direction = models.CharField(max_length=8, choices=DIRECTION_CHOICES)
    confidence_pct = models.IntegerField()
    reason = models.TextField()
    expires_at = models.DateTimeField()


class Order(TimestampedModel):
    signal = models.ForeignKey(Signal, related_name="orders", on_delete=models.CASCADE)
    alpaca_id = models.CharField(max_length=64, unique=True)
    symbol = models.CharField(max_length=16)
    type = models.CharField(max_length=16)
    side = models.CharField(max_length=8)
    qty = models.IntegerField()
    limit_price = models.DecimalField(max_digits=12, decimal_places=4)
    status = models.CharField(max_length=32)
    filled_qty = models.IntegerField(default=0)
    avg_fill_price = models.DecimalField(max_digits=12, decimal_places=4, default=0)


class Position(TimestampedModel):
    symbol = models.CharField(max_length=16)
    side = models.CharField(max_length=8)
    qty = models.IntegerField()
    avg_price = models.DecimalField(max_digits=12, decimal_places=4)
    tp_pct = models.DecimalField(max_digits=5, decimal_places=2)
    sl_pct = models.DecimalField(max_digits=5, decimal_places=2)
    opened_at = models.DateTimeField()
    closed_at = models.DateTimeField(null=True, blank=True)
    pnl_pct = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)


class Config(models.Model):
    key = models.CharField(max_length=128, unique=True)
    value_json = models.JSONField(default=dict)

    def __str__(self) -> str:
        return self.key


class RunLog(TimestampedModel):
    category = models.CharField(max_length=64)
    message = models.CharField(max_length=512)
    payload_json = models.JSONField(default=dict)
    level = models.CharField(max_length=16, default="INFO")


class PatternSnapshot(TimestampedModel):
    symbol = models.CharField(max_length=16)
    window_days = models.IntegerField(default=28)
    features_json = models.JSONField(default=dict)
    verdict = models.CharField(max_length=8)
    confidence_pct = models.IntegerField()


__all__ = [
    "Article",
    "Sentiment",
    "Signal",
    "Order",
    "Position",
    "Config",
    "RunLog",
    "PatternSnapshot",
]
