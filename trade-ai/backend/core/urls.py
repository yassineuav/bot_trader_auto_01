from __future__ import annotations

from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from market.api import viewsets as market_viewsets

router = routers.DefaultRouter()
router.register(r"articles", market_viewsets.ArticleViewSet, basename="article")
router.register(r"sentiments", market_viewsets.SentimentViewSet, basename="sentiment")
router.register(r"signals", market_viewsets.SignalViewSet, basename="signal")
router.register(r"orders", market_viewsets.OrderViewSet, basename="order")
router.register(r"positions", market_viewsets.PositionViewSet, basename="position")
router.register(r"configs", market_viewsets.ConfigViewSet, basename="config")
router.register(r"pattern-snapshots", market_viewsets.PatternSnapshotViewSet, basename="patternsnapshot")
router.register(r"runlogs", market_viewsets.RunLogViewSet, basename="runlog")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include((router.urls, "market"))),
    path("api/news/webhook/<str:provider>/", market_viewsets.NewsWebhookView.as_view(), name="news-webhook"),
    path("api/llm/analyze/", market_viewsets.AnalyzeArticlesView.as_view(), name="llm-analyze"),
    path("api/trading/execute/", market_viewsets.ExecuteSignalView.as_view(), name="execute-signal"),
    path("api/backtest/run/", market_viewsets.BacktestTriggerView.as_view(), name="backtest-run"),
    path("api/backtest/<uuid:pk>/", market_viewsets.BacktestDetailView.as_view(), name="backtest-detail"),
    path("api/account/", market_viewsets.AccountView.as_view(), name="account"),
]
