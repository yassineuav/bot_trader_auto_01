# Testing Guide: Alpaca Client

## Overview

The `backend/market/alpaca/client.py` module has comprehensive test coverage. This guide explains how to run tests and manually verify the client works correctly.

---

## 🧪 Unit Tests

### Location
```
backend/market/tests/test_alpaca_client.py
```

### Running All Tests

**Option 1: Docker Compose**
```bash
cd infra
docker compose run backend python manage.py test market.tests.test_alpaca_client
```

**Option 2: Local Python**
```bash
cd backend
python manage.py test market.tests.test_alpaca_client
```

### Running Specific Test Class

```bash
docker compose run backend python manage.py test market.tests.test_alpaca_client.TestAlpacaClient
```

### Running Specific Test Method

```bash
docker compose run backend python manage.py test market.tests.test_alpaca_client.TestAlpacaClient.test_get_account_success
```

### Running with Verbose Output

```bash
docker compose run backend python manage.py test market.tests.test_alpaca_client --verbosity=2
```

---

## 📋 Test Cases Included

### Initialization Tests
- ✅ `test_client_initialization_with_env_vars` - Client reads from environment
- ✅ `test_client_initialization_with_defaults` - Client has default values
- ✅ `test_headers_include_api_key` - Headers are properly formatted

### Configuration Tests
- ✅ `test_is_configured_true` - Returns true when credentials exist
- ✅ `test_is_configured_false_missing_key` - Returns false when key missing

### API Call Tests
- ✅ `test_get_account_success` - Successfully fetches account data
- ✅ `test_get_account_from_cache` - Returns cached data
- ✅ `test_get_account_request_exception` - Handles connection errors
- ✅ `test_get_account_http_error` - Handles HTTP 401/403 errors

### Portfolio Tests
- ✅ `test_get_portfolio_value` - Correctly transforms portfolio data
- ✅ `test_get_portfolio_value_account_unavailable` - Returns None on failure

### Summary Tests
- ✅ `test_get_account_summary` - Creates proper summary object
- ✅ `test_get_account_summary_missing_fields` - Handles missing fields gracefully

### Cache Tests
- ✅ `test_cache_is_set` - Cache is populated after successful call
- ✅ `test_cache_not_set_on_error` - Cache not set on error

### Data Safety Tests
- ✅ `test_float_conversion_safety` - All floats are safely converted

### Integration Tests
- ✅ `test_real_api_flow_success` - All methods work together

---

## 🖥️ Manual Testing (Django Shell)

### Start Django Shell
```bash
cd backend
python manage.py shell
```

### Test Script
```python
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
    print(f"  Account Value: ${account.get('portfolio_value', 0):,.2f}")
else:
    print("✗ Failed to fetch account")

# 4. Get account summary
summary = client.get_account_summary()
if summary:
    print(f"✓ Summary:")
    print(f"  Status: {summary['status']}")
    print(f"  Account: {summary['account_number']}")
    print(f"  Value: ${summary['account_value']:,.2f}")
    print(f"  Cash: ${summary['cash']:,.2f}")
    print(f"  Buying Power: ${summary['buying_power']:,.2f}")
else:
    print("✗ Failed to fetch summary")

# 5. Get portfolio value
portfolio = client.get_portfolio_value()
if portfolio:
    print(f"✓ Portfolio:")
    print(f"  Account Value: ${portfolio['account_value']:,.2f}")
    print(f"  Cash: ${portfolio['cash']:,.2f}")
    print(f"  Buying Power: ${portfolio['buying_power']:,.2f}")
else:
    print("✗ Failed to fetch portfolio")
```

---

## 🔍 Testing in Docker

### Interactive Testing with Docker

```bash
# Start backend container
docker compose run --rm -it backend python manage.py shell
```

Then paste the manual test script above.

### Running Tests in Docker

```bash
# Run all tests
docker compose run --rm backend python manage.py test market.tests.test_alpaca_client

# Run with coverage
docker compose run --rm backend python -m pytest backend/market/tests/test_alpaca_client.py --cov=market.alpaca

# Run with verbose output
docker compose run --rm backend python manage.py test market.tests.test_alpaca_client --verbosity=2
```

---

## ✅ Verification Checklist

### Before Testing, Verify:

- [ ] `infra/.env` has `ALPACA_API_KEY` set
- [ ] `infra/.env` has `ALPACA_API_SECRET` set
- [ ] `infra/.env` has `ALPACA_BASE_URL` set (or will use default)
- [ ] Docker containers are running: `docker compose up`
- [ ] PostgreSQL is accessible
- [ ] Redis is accessible

### After Testing, Check:

- [ ] All unit tests pass
- [ ] Manual shell test shows account data
- [ ] Account number displays correctly
- [ ] Portfolio value is a float > 0
- [ ] Status is "ACTIVE" or shows error message
- [ ] No timeout errors (check API rate limits)

---

## 🐛 Troubleshooting Test Failures

### Import Error: `market.alpaca.client not found`
```
Solution: Ensure you're in the backend directory when running tests
cd backend
python manage.py test ...
```

### Django settings not configured
```
Solution: Ensure Django settings are available
export DJANGO_SETTINGS_MODULE=core.settings
python manage.py test ...
```

### Database errors
```
Solution: Run migrations first
python manage.py migrate
python manage.py test ...
```

### Redis/Cache errors
```
Solution: Start Redis container
docker compose up redis
# OR run tests with cache disabled
python manage.py test --no-migrations ...
```

### Timeout errors
```
Reason: Alpaca API taking > 10 seconds to respond
Solution: 
1. Check API status: https://status.alpaca.markets
2. Check your internet connection
3. Increase timeout in client.py (currently 10 seconds)
```

### 401/403 Unauthorized errors
```
Reason: Invalid or expired API credentials
Solution:
1. Verify ALPACA_API_KEY in infra/.env
2. Verify ALPACA_API_SECRET in infra/.env
3. Check Alpaca dashboard for credential issues
4. For paper trading, use paper-api.alpaca.markets
```

---

## 📊 Expected Test Output

When all tests pass, you should see:
```
Running tests...
test_cache_is_set (market.tests.test_alpaca_client.TestAlpacaClient) ... ok
test_cache_not_set_on_error (market.tests.test_alpaca_client.TestAlpacaClient) ... ok
test_client_initialization_with_defaults (market.tests.test_alpaca_client.TestAlpacaClient) ... ok
test_client_initialization_with_env_vars (market.tests.test_alpaca_client.TestAlpacaClient) ... ok
test_float_conversion_safety (market.tests.test_alpaca_client.TestAlpacaClient) ... ok
test_get_account_from_cache (market.tests.test_alpaca_client.TestAlpacaClient) ... ok
test_get_account_http_error (market.tests.test_alpaca_client.TestAlpacaClient) ... ok
test_get_account_request_exception (market.tests.test_alpaca_client.TestAlpacaClient) ... ok
test_get_account_success (market.tests.test_alpaca_client.TestAlpacaClient) ... ok
test_get_account_summary (market.tests.test_alpaca_client.TestAlpacaClient) ... ok
test_get_account_summary_missing_fields (market.tests.test_alpaca_client.TestAlpacaClient) ... ok
test_get_portfolio_value (market.tests.test_alpaca_client.TestAlpacaClient) ... ok
test_get_portfolio_value_account_unavailable (market.tests.test_alpaca_client.TestAlpacaClient) ... ok
test_headers_include_api_key (market.tests.test_alpaca_client.TestAlpacaClient) ... ok
test_is_configured_false_missing_key (market.tests.test_alpaca_client.TestAlpacaClient) ... ok
test_is_configured_true (market.tests.test_alpaca_client.TestAlpacaClient) ... ok
test_real_api_flow_success (market.tests.test_alpaca_client.TestAlpacaClientIntegration) ... ok

Ran 17 tests in 0.234s

OK
```

---

## 🎯 What Each Test Validates

| Test | Validates |
|------|-----------|
| Initialization | Environment variables are read correctly |
| Configuration | Credentials are properly loaded |
| Headers | API key is in correct header format |
| Success Path | API call works with valid credentials |
| Caching | Responses are cached for 5 minutes |
| Error Handling | Graceful handling of network errors |
| HTTP Errors | Graceful handling of 401/403 responses |
| Data Transformation | Account data properly transformed |
| Default Values | Missing fields get sensible defaults |
| Type Safety | All numeric values are floats |
| Integration | All methods work together |

---

## 🚀 Next Steps

1. **Run all tests**: `docker compose run backend python manage.py test market.tests`
2. **Check coverage**: Install pytest-cov and run with `--cov` flag
3. **Add more tests**: Add new test methods for edge cases
4. **Monitor in production**: Add logging to client methods

---

## 📞 Support

If tests fail:

1. Check this troubleshooting section first
2. Verify credentials in `infra/.env`
3. Check Django/Docker logs
4. Verify Alpaca API status

All tests use mocked API responses, so they should pass without network issues. Only integration tests need real API access.
