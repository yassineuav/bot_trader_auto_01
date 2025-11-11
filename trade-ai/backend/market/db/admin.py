from django.contrib import admin

from . import models

@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("source", "title", "published_at")
    search_fields = ("title", "body")


@admin.register(models.Sentiment)
class SentimentAdmin(admin.ModelAdmin):
    list_display = ("article", "label", "trend_bull_bear", "trend_strength_pct")


@admin.register(models.Signal)
class SignalAdmin(admin.ModelAdmin):
    list_display = ("symbol", "direction", "source", "confidence_pct", "expires_at")


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("alpaca_id", "symbol", "status", "limit_price")


@admin.register(models.Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("symbol", "side", "qty", "avg_price", "pnl_pct")


@admin.register(models.Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ("key",)


@admin.register(models.RunLog)
class RunLogAdmin(admin.ModelAdmin):
    list_display = ("category", "message", "level", "created_at")


@admin.register(models.PatternSnapshot)
class PatternSnapshotAdmin(admin.ModelAdmin):
    list_display = ("symbol", "window_days", "verdict", "confidence_pct")
