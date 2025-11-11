# Trade AI Monorepo

An end-to-end system that ingests news, analyzes sentiment, generates trading signals, and executes paper option trades with monitoring and dashboards.

## Structure

```
trade-ai/
  backend/        # Django + Celery services
  frontend/       # Next.js dashboard
  infra/          # Docker Compose, env templates, tooling
```

## Quickstart

1. Copy environment template:
   ```bash
   cp infra/.env.example infra/.env
   ```
2. Launch the stack:
   ```bash
   cd infra
   make up
   ```
3. Apply migrations:
   ```bash
   make migrate
   ```
4. Create a Django superuser if desired:
   ```bash
   make createsuperuser
   ```

Backend is available at `http://localhost:8000`, frontend at `http://localhost:3000`.

## Testing

Run backend tests:
```bash
cd backend
pytest
```

Run frontend lint/build:
```bash
cd frontend
npm install
npm run lint
```
