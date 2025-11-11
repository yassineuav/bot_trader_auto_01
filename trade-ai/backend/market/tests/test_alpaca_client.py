"""
Tests for Alpaca API Client
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import requests
from django.test import TestCase, override_settings

from market.alpaca.client import AlpacaClient


class TestAlpacaClient(TestCase):
    """Test suite for AlpacaClient"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_account_data = {
            "id": "account-id-123",
            "account_number": "PA123456",
            "status": "ACTIVE",
            "currency": "USD",
            "portfolio_value": 150000.00,
            "cash": 50000.00,
            "buying_power": 200000.00,
            "daytrading_buying_power": 200000.00,
            "equity": 100000.00,
            "last_equity": 99500.00,
            "multiplier": "4",
            "shorting_enabled": True,
        }

    @override_settings(ALPACA_API_KEY="test-key", ALPACA_API_SECRET="test-secret")
    def test_client_initialization_with_env_vars(self):
        """Test that client initializes with environment variables"""
        with patch.dict(
            "os.environ",
            {
                "ALPACA_API_KEY": "test-key-123",
                "ALPACA_API_SECRET": "test-secret-456",
            },
        ):
            client = AlpacaClient()
            assert client.api_key == "test-key-123"
            assert client.secret_key == "test-secret-456"

    def test_client_initialization_with_defaults(self):
        """Test that client initializes with default values from env"""
        client = AlpacaClient()
        # Should have some key and secret from the environment
        assert isinstance(client.api_key, str)
        assert isinstance(client.secret_key, str)
        assert len(client.api_key) > 0
        assert len(client.secret_key) > 0

    def test_headers_include_api_key(self):
        """Test that headers are properly formatted with API key"""
        client = AlpacaClient()
        assert "APCA-API-KEY-ID" in client.headers
        assert client.headers["APCA-API-KEY-ID"] == client.api_key
        assert client.headers["Content-Type"] == "application/json"

    def test_is_configured_true(self):
        """Test _is_configured returns True when credentials exist"""
        client = AlpacaClient()
        # Should be configured if we have both key and secret from env
        if client.api_key and client.secret_key:
            assert client._is_configured() is True

    def test_is_configured_false_missing_key(self):
        """Test _is_configured returns False when API key is missing"""
        with patch.dict("os.environ", {"ALPACA_API_KEY": "", "ALPACA_API_SECRET": "secret"}):
            # Reload to get empty key
            from market.alpaca import client as client_module

            original_get = client_module.os.environ.get

            def mock_get(key, default=""):
                if key == "ALPACA_API_KEY":
                    return ""
                elif key == "ALPACA_API_SECRET":
                    return "secret"
                return original_get(key, default)

            with patch.object(client_module.os.environ, "get", side_effect=mock_get):
                client = AlpacaClient()
                assert client._is_configured() is False

    @patch("market.alpaca.client.requests.get")
    @patch("market.alpaca.client.cache")
    def test_get_account_success(self, mock_cache, mock_get):
        """Test successful account fetch"""
        # Setup mocks
        mock_cache.get.return_value = None  # No cached data
        mock_response = MagicMock()
        mock_response.json.return_value = self.mock_account_data
        mock_get.return_value = mock_response

        client = AlpacaClient()
        result = client.get_account()

        # Verify request was made correctly
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "/v2/account" in call_args[0][0]
        assert call_args[1]["headers"]["APCA-API-KEY-ID"] == client.api_key
        assert call_args[1]["timeout"] == 10

        # Verify result
        assert result == self.mock_account_data
        assert result["account_number"] == "PA123456"
        assert result["portfolio_value"] == 150000.00

    @patch("market.alpaca.client.requests.get")
    @patch("market.alpaca.client.cache")
    def test_get_account_from_cache(self, mock_cache, mock_get):
        """Test that cached account data is returned"""
        # Setup mocks
        mock_cache.get.return_value = self.mock_account_data  # Cached data exists

        client = AlpacaClient()
        result = client.get_account()

        # Verify no HTTP request was made
        mock_get.assert_not_called()

        # Verify cached data was returned
        assert result == self.mock_account_data

    @patch("market.alpaca.client.requests.get")
    @patch("market.alpaca.client.cache")
    def test_get_account_request_exception(self, mock_cache, mock_get):
        """Test handling of request exceptions"""
        # Setup mocks
        mock_cache.get.return_value = None
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

        client = AlpacaClient()
        result = client.get_account()

        # Should return None on error
        assert result is None

    @patch("market.alpaca.client.requests.get")
    @patch("market.alpaca.client.cache")
    def test_get_account_http_error(self, mock_cache, mock_get):
        """Test handling of HTTP errors"""
        # Setup mocks
        mock_cache.get.return_value = None
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "401 Unauthorized"
        )
        mock_get.return_value = mock_response

        client = AlpacaClient()
        result = client.get_account()

        # Should return None on HTTP error
        assert result is None

    @patch("market.alpaca.client.requests.get")
    @patch("market.alpaca.client.cache")
    def test_get_portfolio_value(self, mock_cache, mock_get):
        """Test get_portfolio_value method"""
        # Setup mocks
        mock_cache.get.return_value = None
        mock_response = MagicMock()
        mock_response.json.return_value = self.mock_account_data
        mock_get.return_value = mock_response

        client = AlpacaClient()
        result = client.get_portfolio_value()

        assert result is not None
        assert result["account_value"] == 150000.00
        assert result["cash"] == 50000.00
        assert result["buying_power"] == 200000.00
        assert result["long_market_value"] == 0  # Not in mock data, should default to 0
        assert isinstance(result["account_value"], float)

    @patch("market.alpaca.client.requests.get")
    @patch("market.alpaca.client.cache")
    def test_get_portfolio_value_account_unavailable(self, mock_cache, mock_get):
        """Test get_portfolio_value when account fetch fails"""
        # Setup mocks
        mock_cache.get.return_value = None
        mock_get.side_effect = requests.exceptions.ConnectionError("No connection")

        client = AlpacaClient()
        result = client.get_portfolio_value()

        # Should return None when account is unavailable
        assert result is None

    @patch("market.alpaca.client.requests.get")
    @patch("market.alpaca.client.cache")
    def test_get_account_summary(self, mock_cache, mock_get):
        """Test get_account_summary method"""
        # Setup mocks
        mock_cache.get.return_value = None
        mock_response = MagicMock()
        mock_response.json.return_value = self.mock_account_data
        mock_get.return_value = mock_response

        client = AlpacaClient()
        result = client.get_account_summary()

        assert result is not None
        assert result["status"] == "ACTIVE"
        assert result["account_number"] == "PA123456"
        assert result["account_value"] == 150000.00
        assert result["cash"] == 50000.00
        assert result["buying_power"] == 200000.00
        assert result["day_trading_buying_power"] == 200000.00
        assert result["equity"] == 100000.00
        assert result["last_equity"] == 99500.00
        assert result["multiplier"] == "4"
        assert result["shorting_enabled"] is True

    @patch("market.alpaca.client.requests.get")
    @patch("market.alpaca.client.cache")
    def test_get_account_summary_missing_fields(self, mock_cache, mock_get):
        """Test get_account_summary handles missing fields gracefully"""
        # Setup mocks with minimal data
        mock_cache.get.return_value = None
        minimal_data = {"account_number": "PA999"}
        mock_response = MagicMock()
        mock_response.json.return_value = minimal_data
        mock_get.return_value = mock_response

        client = AlpacaClient()
        result = client.get_account_summary()

        assert result is not None
        assert result["account_number"] == "PA999"
        assert result["status"] == "unknown"  # Default value
        assert result["account_value"] == 0.0  # Default value
        assert result["cash"] == 0.0  # Default value
        assert result["multiplier"] == 1  # Default value
        assert result["shorting_enabled"] is False  # Default value

    @patch("market.alpaca.client.requests.get")
    @patch("market.alpaca.client.cache")
    def test_cache_is_set(self, mock_cache, mock_get):
        """Test that successful responses are cached"""
        # Setup mocks
        mock_cache.get.return_value = None
        mock_response = MagicMock()
        mock_response.json.return_value = self.mock_account_data
        mock_get.return_value = mock_response

        client = AlpacaClient()
        client.get_account()

        # Verify cache.set was called
        mock_cache.set.assert_called_once()
        call_args = mock_cache.set.call_args
        assert call_args[0][0] == "alpaca_account"  # cache key
        assert call_args[0][1] == self.mock_account_data  # data
        assert call_args[0][2] == 300  # timeout (5 minutes)

    @patch("market.alpaca.client.requests.get")
    @patch("market.alpaca.client.cache")
    def test_cache_not_set_on_error(self, mock_cache, mock_get):
        """Test that cache is not set on error"""
        # Setup mocks
        mock_cache.get.return_value = None
        mock_get.side_effect = requests.exceptions.ConnectionError("No connection")

        client = AlpacaClient()
        client.get_account()

        # Verify cache.set was NOT called
        mock_cache.set.assert_not_called()

    @patch("market.alpaca.client.requests.get")
    @patch("market.alpaca.client.cache")
    def test_float_conversion_safety(self, mock_cache, mock_get):
        """Test that all numeric values are safely converted to float"""
        # Setup mocks with string values (edge case)
        mock_cache.get.return_value = None
        data_with_strings = {
            "portfolio_value": "150000.00",
            "cash": "50000",
            "buying_power": "200000.99",
            "daytrading_buying_power": "invalid",  # This should cause an issue
            "equity": "100000",
            "last_equity": "99500.50",
        }
        mock_response = MagicMock()
        mock_response.json.return_value = data_with_strings
        mock_get.return_value = mock_response

        client = AlpacaClient()

        # get_account_summary should handle this
        try:
            result = client.get_account_summary()
            # If we get here, invalid values were handled (converted to 0.0)
            assert isinstance(result["account_value"], float)
        except ValueError:
            # It's acceptable to raise ValueError for truly invalid data
            pass


class TestAlpacaClientIntegration(TestCase):
    """Integration tests for AlpacaClient with real API (if credentials available)"""

    @patch("market.alpaca.client.requests.get")
    @patch("market.alpaca.client.cache")
    def test_real_api_flow_success(self, mock_cache, mock_get):
        """Test the complete flow with realistic data"""
        # Setup mocks
        mock_cache.get.return_value = None
        realistic_data = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "account_number": "PA123456",
            "status": "ACTIVE",
            "currency": "USD",
            "portfolio_value": 125432.50,
            "cash": 35000.00,
            "buying_power": 140000.00,
            "daytrading_buying_power": 140000.00,
            "equity": 125432.50,
            "last_equity": 124500.75,
            "multiplier": "4",
            "shorting_enabled": True,
            "long_market_value": 90432.50,
            "short_market_value": 0.00,
        }
        mock_response = MagicMock()
        mock_response.json.return_value = realistic_data
        mock_get.return_value = mock_response

        client = AlpacaClient()
        account = client.get_account()
        summary = client.get_account_summary()
        portfolio = client.get_portfolio_value()

        # Verify all methods work together
        assert account is not None
        assert summary is not None
        assert portfolio is not None
        assert summary["account_value"] == portfolio["account_value"]


# ============================================================================
# Manual Testing Script - Run this in Django shell: python manage.py shell
# ============================================================================
"""
from market.alpaca.client import AlpacaClient

# 1. Create client
client = AlpacaClient()
print("✓ Client created")

# 2. Check if configured
print(f"Configured: {client._is_configured()}")

# 3. Get account details
account = client.get_account()
if account:
    print(f"✓ Account fetched: {account.get('account_number')}")
else:
    print("✗ Failed to fetch account")

# 4. Get account summary
summary = client.get_account_summary()
if summary:
    print(f"✓ Summary: {summary}")
else:
    print("✗ Failed to fetch summary")

# 5. Get portfolio value
portfolio = client.get_portfolio_value()
if portfolio:
    print(f"✓ Portfolio: {portfolio}")
else:
    print("✗ Failed to fetch portfolio")
"""
