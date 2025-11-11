from __future__ import annotations

import logging
from typing import Optional, Dict, Any

import requests
from django.core.cache import cache

from market.utils.config import get_config_value

logger = logging.getLogger(__name__)

ALPACA_BASE_URL = "https://paper-api.alpaca.markets"
CACHE_TIMEOUT = 300  # 5 minutes


class AlpacaClient:
    """Client for interacting with Alpaca API"""

    def __init__(self):
        self.api_key = get_config_value("ALPACA_API_KEY", "")
        self.secret_key = get_config_value("ALPACA_SECRET_KEY", "")
        self.base_url = ALPACA_BASE_URL
        self.headers = {
            "APCA-API-KEY-ID": self.api_key,
            "Content-Type": "application/json",
        }

    def _is_configured(self) -> bool:
        """Check if API credentials are configured"""
        return bool(self.api_key and self.secret_key)

    def get_account(self) -> Optional[Dict[str, Any]]:
        """Fetch account details from Alpaca API"""
        if not self._is_configured():
            logger.warning("Alpaca API credentials not configured")
            return None

        cache_key = "alpaca_account"
        cached = cache.get(cache_key)
        if cached:
            return cached

        try:
            response = requests.get(
                f"{self.base_url}/v2/account",
                headers=self.headers,
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            cache.set(cache_key, data, CACHE_TIMEOUT)
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch Alpaca account: {e}")
            return None

    def get_portfolio_value(self) -> Optional[Dict[str, Any]]:
        """Fetch portfolio value details"""
        account = self.get_account()
        if not account:
            return None

        return {
            "account_value": float(account.get("portfolio_value", 0)),
            "cash": float(account.get("cash", 0)),
            "buying_power": float(account.get("buying_power", 0)),
            "long_market_value": float(account.get("long_market_value", 0)),
            "short_market_value": float(account.get("short_market_value", 0)),
        }

    def get_account_summary(self) -> Optional[Dict[str, Any]]:
        """Get a summary of account information"""
        account = self.get_account()
        if not account:
            return None

        return {
            "status": account.get("status", "unknown"),
            "account_number": account.get("account_number", "N/A"),
            "account_value": float(account.get("portfolio_value", 0)),
            "cash": float(account.get("cash", 0)),
            "buying_power": float(account.get("buying_power", 0)),
            "day_trading_buying_power": float(account.get("daytrading_buying_power", 0)),
            "equity": float(account.get("equity", 0)),
            "last_equity": float(account.get("last_equity", 0)),
            "multiplier": account.get("multiplier", 1),
            "shorting_enabled": account.get("shorting_enabled", False),
        }

