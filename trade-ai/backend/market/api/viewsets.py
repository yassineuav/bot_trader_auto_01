from __future__ import annotations

import datetime as dt
from uuid import uuid4

from django.utils import timezone
from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from market.db import models
from . import serializers
from ..llm import analyzer
from ..news import ingest
from ..signals import generator
from ..trading import executor
from ..ml import patterns
from scripts import backtest_runner


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer


class SentimentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Sentiment.objects.select_related("article").all()
    serializer_class = serializers.SentimentSerializer


class SignalViewSet(viewsets.ModelViewSet):
    queryset = models.Signal.objects.all()
    serializer_class = serializers.SignalSerializer

    @action(detail=False, methods=["get"])
    def latest(self, request):
        symbol = request.query_params.get("symbol")
        qs = self.get_queryset()
        if symbol:
            qs = qs.filter(symbol=symbol)
        serializer = self.get_serializer(qs.order_by("-created_at")[:20], many=True)
        return Response(serializer.data)


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Order.objects.select_related("signal").all()
    serializer_class = serializers.OrderSerializer


class PositionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Position.objects.all()
    serializer_class = serializers.PositionSerializer


class ConfigViewSet(viewsets.ModelViewSet):
    queryset = models.Config.objects.all()
    serializer_class = serializers.ConfigSerializer
    lookup_field = "key"


class RunLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.RunLog.objects.all()
    serializer_class = serializers.RunLogSerializer


class PatternSnapshotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.PatternSnapshot.objects.all()
    serializer_class = serializers.PatternSnapshotSerializer


class NewsWebhookView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, provider: str) -> Response:
        raw_articles = request.data if isinstance(request.data, list) else [request.data]
        created = ingest.save_articles_from_webhook(provider, raw_articles)
        return Response({"created": created})


class AnalyzeArticlesView(generics.GenericAPIView):
    def post(self, request) -> Response:
        article_ids = request.data.get("article_ids", [])
        articles = models.Article.objects.filter(id__in=article_ids)
        sentiments = analyzer.analyze_articles(articles)
        serializer = serializers.SentimentSerializer(sentiments, many=True)
        return Response(serializer.data)


class ExecuteSignalView(generics.GenericAPIView):
    def post(self, request) -> Response:
        signal_id = request.data.get("signal_id")
        signal = models.Signal.objects.get(id=signal_id)
        order = executor.execute_signal(signal)
        serializer = serializers.OrderSerializer(order)
        return Response(serializer.data)


class BacktestTriggerView(generics.GenericAPIView):
    def post(self, request) -> Response:
        params = request.data
        job_id = backtest_runner.enqueue_backtest(params)
        return Response({"job_id": str(job_id)})


class BacktestDetailView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        record = backtest_runner.get_backtest_result(pk)
        if not record:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(record)
