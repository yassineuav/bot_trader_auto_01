# AlpacaClient Testing - Quick Reference

## 🚀 Quick Start

### Run All Tests
```bash
docker compose run backend python manage.py test market.tests.test_alpaca_client
```

### Run Specific Test
```bash
docker compose run backend python manage.py test market.tests.test_alpaca_client.TestAlpacaClient.test_get_account_success
```

### Manual Test (Django Shell)
```bash
docker compose run backend python manage.py shell
```

Then paste:
```python
from market.alpaca.client import AlpacaClient

client = AlpacaClient()
print(f"Configured: {client._is_configured()}")
print(f"Account: {client.get_account_summary()}")
```

---

## 📊 Test Coverage

**17 Unit Tests** covering:
- ✅ Client initialization
- ✅ Credential configuration
- ✅ API calls & responses
- ✅ Error handling
- ✅ Caching behavior
- ✅ Data transformation
- ✅ Default values
- ✅ Type safety

---

## 🎯 Key Methods Being Tested

| Method | Purpose | Tests |
|--------|---------|-------|
| `__init__()` | Initialize client | 2 |
| `_is_configured()` | Check credentials exist | 2 |
| `get_account()` | Fetch from Alpaca API | 5 |
| `get_portfolio_value()` | Get portfolio summary | 2 |
| `get_account_summary()` | Get formatted summary | 4 |

---

## ✅ What's Tested

### ✓ Success Cases
- Client initializes with env vars
- API call returns valid data
- Data is properly transformed
- Cache works correctly

### ✓ Error Cases
- Connection errors handled gracefully
- HTTP 401/403 errors handled
- Missing fields use default values
- Invalid data types converted safely

### ✓ Integration
- All methods work together
- Realistic API flow validated

---

## 📋 Test File Location

```
backend/market/tests/test_alpaca_client.py
```

**Lines**: ~380  
**Test Classes**: 2 (TestAlpacaClient, TestAlpacaClientIntegration)  
**Test Methods**: 17  

---

## 🔧 Testing Options

### Option 1: Unit Tests (Recommended)
```bash
docker compose run backend python manage.py test market.tests.test_alpaca_client
```
✅ Fast (~1 sec)  
✅ All mocked  
✅ No API calls  
✅ Repeatable  

### Option 2: Django Shell (Manual)
```bash
docker compose run backend python manage.py shell
```
✅ Interactive  
✅ Real API calls  
✅ See actual data  
❌ Slower  

### Option 3: Verbose Testing
```bash
docker compose run backend python manage.py test market.tests.test_alpaca_client --verbosity=2
```
✅ See all test names  
✅ Detailed output  

---

## ⚡ Common Issues

| Issue | Solution |
|-------|----------|
| Import Error | Run from backend dir |
| DB Error | Run migrations first |
| Cache Error | Start Redis container |
| API Error (401) | Check credentials in `.env` |
| Timeout | Check API status |

---

## 📈 Test Results

All tests use **mocked responses** so they:
- Don't require real API access
- Run in < 1 second
- Are 100% deterministic
- Can run offline

Expected: **17 passed in ~0.2s**

---

## 🎓 Learn More

Full testing guide: `TESTING_GUIDE.md`

---

**Status**: ✅ Ready to test  
**Last Updated**: November 11, 2025
