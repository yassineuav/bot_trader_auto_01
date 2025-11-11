# API Endpoint Mapping - Backend ↔ Frontend

## Architecture

```
Frontend Browser
    ↓
Frontend Route Handler (/api/...)
    ↓
Backend Django REST API (/api/...)
    ↓
Database / External APIs
```

---

## Backend Endpoints (Django REST API)

All endpoints use `/api/` prefix and return JSON responses.

### Articles
- **GET** `/api/articles/` - List all articles
- **GET** `/api/articles/{id}/` - Get single article
- **POST** `/api/articles/` - Create article
- **PUT** `/api/articles/{id}/` - Update article
- **DELETE** `/api/articles/{id}/` - Delete article

### Sentiments
- **GET** `/api/sentiments/` - List all sentiments
- **GET** `/api/sentiments/{id}/` - Get single sentiment
- **POST** `/api/sentiments/` - Create sentiment
- **PUT** `/api/sentiments/{id}/` - Update sentiment
- **DELETE** `/api/sentiments/{id}/` - Delete sentiment

### Signals
- **GET** `/api/signals/` - List all signals
- **GET** `/api/signals/?symbol=SPY` - Filter by symbol
- **GET** `/api/signals/latest/` - Get 20 latest signals
- **GET** `/api/signals/latest/?symbol=SPY` - Get latest for symbol
- **GET** `/api/signals/{id}/` - Get single signal
- **POST** `/api/signals/` - Create signal
- **PUT** `/api/signals/{id}/` - Update signal
- **DELETE** `/api/signals/{id}/` - Delete signal

### Orders
- **GET** `/api/orders/` - List all orders
- **GET** `/api/orders/{id}/` - Get single order
- **POST** `/api/orders/` - Create order
- **PUT** `/api/orders/{id}/` - Update order
- **DELETE** `/api/orders/{id}/` - Delete order

### Positions
- **GET** `/api/positions/` - List all positions
- **GET** `/api/positions/{id}/` - Get single position
- **POST** `/api/positions/` - Create position
- **PUT** `/api/positions/{id}/` - Update position
- **DELETE** `/api/positions/{id}/` - Delete position

### Configuration
- **GET** `/api/configs/` - List all configs
- **GET** `/api/configs/{id}/` - Get single config
- **POST** `/api/configs/` - Create config
- **PUT** `/api/configs/{id}/` - Update config
- **DELETE** `/api/configs/{id}/` - Delete config

### Pattern Snapshots
- **GET** `/api/pattern-snapshots/` - List all patterns
- **GET** `/api/pattern-snapshots/{id}/` - Get single pattern
- **POST** `/api/pattern-snapshots/` - Create pattern
- **PUT** `/api/pattern-snapshots/{id}/` - Update pattern
- **DELETE** `/api/pattern-snapshots/{id}/` - Delete pattern

### Run Logs
- **GET** `/api/runlogs/` - List all run logs
- **GET** `/api/runlogs/{id}/` - Get single run log

### Account (Alpaca)
- **GET** `/api/account/` - Get account details from Alpaca

### News
- **POST** `/api/news/webhook/{provider}/` - Webhook for news ingestion

### LLM Analysis
- **POST** `/api/llm/analyze/` - Analyze articles with LLM

### Trading Execution
- **POST** `/api/trading/execute/` - Execute trading signal

### Backtesting
- **GET** `/api/backtest/` - List all backtests
- **POST** `/api/backtest/run/` - Run new backtest
- **GET** `/api/backtest/{id}/` - Get backtest details
- **DELETE** `/api/backtest/{id}/` - Delete backtest

---

## Frontend Routes (Next.js API Routes)

These are server-side proxies that call the backend.

### `/app/api/signals/latest/route.ts`
- **Calls**: `GET /api/signals/latest/` on backend
- **Returns**: Array of latest signals

### `/app/api/signals/route.ts`
- **Calls**: `GET /api/signals/` on backend
- **Returns**: Array of all signals

### `/app/api/orders/route.ts`
- **Calls**: `GET /api/orders/` on backend
- **Returns**: Array of all orders

### `/app/api/positions/route.ts`
- **Calls**: `GET /api/positions/` on backend
- **Returns**: Array of all positions

### `/app/api/account/route.ts`
- **Calls**: `GET /api/account/` on backend
- **Returns**: Account details object

### `/app/api/config/route.ts`
- **Calls**: `GET /api/configs/` on backend
- **Returns**: Array of configs

### `/app/api/news/route.ts`
- **Calls**: `GET /api/articles/` on backend
- **Returns**: Array of articles

### `/app/api/dashboard/kpis/route.ts`
- **Calls**: `GET /api/signals/latest/` on backend
- **Aggregates**: KPI data
- **Returns**: Dashboard metrics object

### `/app/api/backtests/route.ts`
- **Calls**: `GET /api/backtest/` on backend
- **Returns**: Array of backtests

### `/app/api/backtests/[id]/route.ts`
- **Calls**: `GET /api/backtest/{id}/` on backend
- **Returns**: Single backtest object

---

## Response Format Standards

### Success Response (200)
```json
{
  "data": { /* actual data */ },
  "status": "success",
  "message": "Operation completed"
}
```

OR for list endpoints:
```json
[
  { "id": 1, "name": "item1", ... },
  { "id": 2, "name": "item2", ... }
]
```

### Error Response
```json
{
  "error": "Error message",
  "status": "error",
  "code": "ERROR_CODE"
}
```

---

## Frontend ↔ Backend Calling Pattern

```
1. Browser requests: GET /api/signals/latest
2. Frontend route: /app/api/signals/latest/route.ts
3. Frontend calls backend: GET /api/signals/latest/
4. Django ViewSet returns data
5. Frontend returns JSON to browser
```

### Example Flow

**Frontend Component** (`recent-signals.tsx`):
```typescript
const response = await fetch('/api/signals/latest');
const signals = await response.json();
```

**Frontend Route** (`/app/api/signals/latest/route.ts`):
```typescript
const data = await backendFetch("/api/signals/latest/");
return Response.json(data);
```

**Backend** (`/api/signals/latest/`):
```python
def latest(self, request):
    qs = self.get_queryset().order_by("-created_at")[:20]
    serializer = self.get_serializer(qs, many=True)
    return Response(serializer.data)
```

---

## Configuration

### Environment Variables (backend/.env)

```
# Django
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=false

# Database
DATABASE_URL=postgres://user:pass@db:5432/tradeai

# Redis/Cache
REDIS_URL=redis://redis:6379/0

# Alpaca
ALPACA_API_KEY=your_key
ALPACA_API_SECRET=your_secret
ALPACA_BASE_URL=https://paper-api.alpaca.markets

# API
ALLOWED_HOSTS=localhost,127.0.0.1,backend,frontend

# LLM
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o-mini
```

---

## Common Patterns

### Filtering
```
/api/signals/?symbol=SPY
/api/orders/?status=FILLED
/api/articles/?source=BENZINGA
```

### Pagination
```
/api/signals/?page=1&page_size=20
/api/orders/?limit=50&offset=0
```

### Ordering
```
/api/signals/?ordering=-created_at
/api/orders/?ordering=created_at
```

---

## Error Handling

### 401 Unauthorized
- Missing or invalid authentication token
- Solution: Check credentials in .env

### 403 Forbidden
- Request not allowed by permissions
- Solution: Check DEFAULT_PERMISSION_CLASSES in settings.py

### 404 Not Found
- Resource does not exist
- Solution: Verify endpoint path and ID

### 500 Internal Server Error
- Server error processing request
- Solution: Check backend logs with `docker compose logs backend`

### Connection Refused
- Backend not running
- Solution: Run `docker compose up` in infra/ directory

---

## Testing Endpoints

### Using curl (from terminal)

```bash
# Get latest signals
curl http://localhost:8000/api/signals/latest/

# Get all orders
curl http://localhost:8000/api/orders/

# Get account details
curl http://localhost:8000/api/account/

# Get dashboard KPIs
curl http://localhost:3000/api/dashboard/kpis
```

### Using browser

```
http://localhost:3000/api/signals/latest
http://localhost:3000/api/orders
http://localhost:3000/api/positions
http://localhost:3000/api/account
```

---

## Summary

✅ All frontend routes have matching backend endpoints  
✅ Naming is consistent: `/api/resource/`  
✅ HTTP methods match REST conventions  
✅ Error handling is standardized  
✅ Environment variables are properly loaded  

**Status**: Production Ready
