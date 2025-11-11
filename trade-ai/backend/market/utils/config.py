from __future__ import annotations

from market.db import models


def get_config_value(key: str, default):
    cfg = models.Config.objects.filter(key=key).first()
    if cfg:
        return cfg.value_json.get("value", default)
    return default
