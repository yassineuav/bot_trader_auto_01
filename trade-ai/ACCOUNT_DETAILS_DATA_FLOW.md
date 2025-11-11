# Alpaca Account Details Integration - Data Flow Documentation

## Overview
This document describes the complete data flow for displaying Alpaca account details in the trading dashboard.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         DASHBOARD                               │
│              (frontend/app/(dashboard)/dashboard/page.tsx)       │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  AccountDetails Component                                │  │
│  │  (frontend/components/account-details.tsx)               │  │
│  │  - Fetches from /api/account                             │  │
│  │  - Auto-refreshes every 30 seconds                       │  │
│  │  - Displays account metrics with color indicators        │  │
│  │  - Shows warnings for missing credentials               │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│            FRONTEND API ROUTE                                    │
│     (frontend/app/api/account/route.ts)                          │
│  - Receives GET request from client                              │
│  - Calls backend at /api/account/                                │
│  - Maps response fields                                          │
│  - Returns JSON to client                                        │
└──────────────────────┬───────────────────────────────────────────┘
                       │
      ┌────────────────┴────────────────┐
      │     BACKEND SERVER             │
      │     (Django REST API)           │
      ▼                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│           DJANGO BACKEND URLS                                    │
│        (backend/core/urls.py)                                    │
│                                                                  │
│  path("api/account/", AccountView.as_view(), name="account")    │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│            ACCOUNT VIEW                                          │
│     (backend/market/api/viewsets.py)                             │
│  - Checks credentials via _is_configured()                       │
│  - Calls client.get_account_summary()                            │
│  - Handles error cases gracefully                                │
│  - Returns JSON response with all fields                         │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│            ALPACA CLIENT                                         │
│     (backend/market/alpaca/client.py)                            │
│  - AlpacaClient class                                            │
│  - _is_configured(): Checks API credentials                      │
│  - get_account(): Fetches raw data from Alpaca API               │
│  - get_account_summary(): Transforms data with safe defaults     │
│  - Caches results for 5 minutes                                  │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│            ALPACA API (External)                                 │
│        https://paper-api.alpaca.markets                          │
│  - GET /v2/account - Retrieves account details                   │
│  - Requires: ALPACA_API_KEY header                               │
└──────────────────────────────────────────────────────────────────┘
```

## Detailed Data Flow

### 1. Client-Side Initialization (AccountDetails Component)
- Component mounts on dashboard page
- Uses SWR hook to fetch data from `/api/account`
- Auto-refresh configured for 30-second intervals
- Manual refresh button available

### 2. Frontend API Route Processing
- Receives GET request from client
- Calls backend API at `http://backend:8000/api/account/`
- Maps backend response to frontend format
- Provides fallback values if backend is unavailable

### 3. Backend Request Processing (AccountView)
- Receives request from frontend
- Creates AlpacaClient instance
- Checks if credentials are configured:
  - If not configured: Returns "not_configured" status
  - If available: Calls `get_account_summary()`
- Serializes response using AccountSummarySerializer
- Returns JSON response

### 4. Alpaca Client Operations (AlpacaClient)
- Gets API credentials from Django config
- Checks if credentials are present via `_is_configured()`
- Attempts to fetch cached account data (5-minute cache)
- If not cached, calls Alpaca API via HTTPS
- Transforms raw Alpaca response with safe float conversions
- Returns structured account data

### 5. Frontend Component Rendering
- Receives data from `/api/account`
- Calculates derived metrics (Unrealized P&L)
- Applies color indicators based on status/values
- Displays error messages if needed
- Shows last update timestamp

## Data Structure

### Request Flow
```
Frontend Component → GET /api/account → Frontend Route → Backend (/api/account/)
```

### Response Structure
```json
{
  "status": "active|not_configured|unavailable|error",
  "account_number": "string",
  "account_value": number,
  "cash": number,
  "buying_power": number,
  "day_trading_buying_power": number,
  "equity": number,
  "last_equity": number,
  "multiplier": number,
  "shorting_enabled": boolean
}
```

## Error Handling

### Case 1: Missing Credentials
- **Detection**: `_is_configured()` returns False
- **Response Status**: "not_configured"
- **Frontend Action**: Shows yellow warning banner
- **HTTP Status**: 200 (success, with data)

### Case 2: Alpaca API Unreachable
- **Detection**: requests.get() raises exception
- **Response Status**: "unavailable"
- **Frontend Action**: Shows red error banner
- **HTTP Status**: 200 (success, with fallback data)

### Case 3: Network Error
- **Detection**: Frontend fetch fails
- **Response Status**: "error"
- **Frontend Action**: Uses default values
- **HTTP Status**: 200 (fallback)

## Environment Configuration

Required environment variables (in `infra/.env`):
```
ALPACA_API_KEY=your_api_key_here
ALPACA_API_SECRET=your_api_secret_here
```

These are loaded by Django settings from `infra/.env` file.

## Caching

- Alpaca API responses cached for 5 minutes
- Cache key: `alpaca_account`
- Django cache backend (default: database cache)
- Can be cleared manually if needed

## Component Props & Features

### AccountDetails Component Features
- **Auto-Refresh**: 30 seconds
- **Manual Refresh**: Button available in header
- **Color Indicators**:
  - Green: Active status, positive P&L
  - Yellow: Not configured warnings
  - Red: Errors, unavailable, negative P&L
- **Highlighted Fields**: Account Value, Status, Equity, P&L
- **Calculated Metrics**: Unrealized P&L percentage
- **Loading State**: Shows "Loading account details..."
- **Timestamp**: Shows last update time

## Testing Checklist

- [ ] API credentials configured in `infra/.env`
- [ ] Django migrations applied (`python manage.py migrate`)
- [ ] Alpaca API key valid and not expired
- [ ] Frontend component loads without errors
- [ ] Data updates every 30 seconds
- [ ] Manual refresh button works
- [ ] Error messages appear when credentials missing
- [ ] Handles network failures gracefully
- [ ] Formatting displays correctly (currency, percentages)

## Files Involved

### Backend
- `backend/market/alpaca/client.py` - AlpacaClient class
- `backend/market/api/viewsets.py` - AccountView endpoint
- `backend/market/api/serializers.py` - AccountSummarySerializer
- `backend/core/urls.py` - URL routing
- `backend/core/settings.py` - Django settings with .env loading

### Frontend
- `frontend/components/account-details.tsx` - Main component
- `frontend/app/api/account/route.ts` - API route handler
- `frontend/app/(dashboard)/dashboard/page.tsx` - Dashboard page
- `frontend/lib/server-api.ts` - Backend fetch utility
- `frontend/tsconfig.json` - Path aliases config

## Troubleshooting

### Account data shows as N/A
1. Check if API credentials are in `infra/.env`
2. Verify credentials are correct (try in Alpaca dashboard)
3. Check Django logs for error messages

### Data not refreshing
1. Check browser console for fetch errors
2. Verify backend server is running
3. Check CORS configuration in Django settings

### Status shows "not_configured"
1. Add ALPACA_API_KEY and ALPACA_API_SECRET to `infra/.env`
2. Restart Django server to reload environment
3. Verify keys in Django admin under Config model

### Status shows "unavailable"
1. Check Alpaca API status
2. Verify API key has account permissions
3. Check firewall/proxy isn't blocking requests
