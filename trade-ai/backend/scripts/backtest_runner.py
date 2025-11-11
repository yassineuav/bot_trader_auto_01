from __future__ import annotations

import uuid
from typing import Dict

from django.utils import timezone

_BACKTEST_RESULTS: dict[uuid.UUID, dict] = {}


def enqueue_backtest(params: dict) -> uuid.UUID:
    job_id = uuid.uuid4()
    result = run_backtest(params)
    _BACKTEST_RESULTS[job_id] = result
    return job_id


def get_backtest_result(job_id: str | uuid.UUID) -> dict | None:
    job_uuid = uuid.UUID(str(job_id))
    return _BACKTEST_RESULTS.get(job_uuid)


def run_backtest(params: dict) -> dict:
    symbol = params.get("symbol", "SPY")
    start = params.get("start", "2023-01-01")
    end = params.get("end", timezone.now().date().isoformat())
    mode = params.get("mode", "news")
    trades = 10
    wins = 6
    win_rate = wins / trades if trades else 0
    return {
        "symbol": symbol,
        "start": start,
        "end": end,
        "mode": mode,
        "metrics": {
            "trades": trades,
            "win_rate": win_rate,
            "avg_pl": 0.12,
            "max_drawdown": -0.05,
            "sharpe": 1.2,
        },
    }
