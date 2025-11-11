from __future__ import annotations

from rest_framework import serializers

from market.db import models


class SentimentSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sentiment
        fields = ("id", "label", "trend_bull_bear", "trend_strength_pct", "created_at")


class ArticleSerializer(serializers.ModelSerializer):
    sentiments = SentimentSummarySerializer(many=True, read_only=True)

    class Meta:
        model = models.Article
        fields = "__all__"


class SentimentSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(read_only=True)

    class Meta:
        model = models.Sentiment
        fields = "__all__"


class SignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Signal
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = "__all__"


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Position
        fields = "__all__"


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Config
        fields = "__all__"


class RunLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RunLog
        fields = "__all__"


class PatternSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PatternSnapshot
        fields = "__all__"
