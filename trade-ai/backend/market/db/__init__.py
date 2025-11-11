from django.apps import AppConfig


class MarketDbConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "market.db"
    verbose_name = "Market Database"

    def ready(self) -> None:  # pragma: no cover
        from . import signals  # noqa: F401
