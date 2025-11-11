from __future__ import annotations

import decimal
import logging
from dataclasses import dataclass

import requests
from django.utils import timezone

from market.db import models
from ..utils.config import get_config_value

logger = logging.getLogger(__name__)

ALPACA_BASE_URL = "https://paper-api.alpaca.markets"
ALPACA_DATA_URL = "https://data.alpaca.markets"


@dataclass
class OptionContract:
    symbol: str
    expiry: str
    strike: float
    option_type: str


def _select_contract(symbol: str, direction: str) -> OptionContract:
    # TODO: Replace with Alpaca options chain query.
    expiry = (timezone.now() + timezone.timedelta(days=7)).strftime("%Y-%m-%d")
    strike = 0
    option_type = "call" if direction == "call" else "put"
    return OptionContract(symbol=f"{symbol}{expiry}{option_type.upper()}", expiry=expiry, strike=strike, option_type=option_type)


def execute_signal(signal: models.Signal) -> models.Order:
    contract = _select_contract(signal.symbol, signal.direction)
    account_risk_pct = decimal.Decimal(str(get_config_value("ACCOUNT_RISK_PCT", 0.1)))
    account_buying_power = decimal.Decimal("100000")  # TODO: fetch from Alpaca account endpoint
    notional = (account_buying_power * account_risk_pct).quantize(decimal.Decimal("0.01"))
    limit_price = decimal.Decimal("1.00")
    qty = max(int(notional / limit_price), 1)
    alpaca_id = f"paper-{signal.id}"
    order = models.Order.objects.create(
        signal=signal,
        alpaca_id=alpaca_id,
        symbol=contract.symbol,
        type="option",
        side="buy" if signal.direction == "call" else "sell",
        qty=qty,
        limit_price=limit_price,
        status="filled",
        filled_qty=qty,
        avg_fill_price=limit_price,
    )
    models.Position.objects.create(
        symbol=signal.symbol,
        side="long" if signal.direction == "call" else "short",
        qty=qty,
        avg_price=limit_price,
        tp_pct=get_config_value("TP_PCT", 0.5) * 100,
        sl_pct=get_config_value("SL_PCT", 0.1) * 100,
        opened_at=timezone.now(),
    )
    return order
