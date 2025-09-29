# Unified Connector Platform - Backend Service

FastAPI backend exposing REST endpoints:
- /auth/api-key (POST): Authenticate with API key
- /auth/oauth/init (POST): Initiate OAuth flow
- /auth/oauth/callback (POST): Complete OAuth flow
- /connectors (GET, POST): List/Create connectors
- /connectors/{id} (GET, PATCH, DELETE): Get/Update/Delete connector
- /llm-proxy (POST): Invoke LLM tool through provider proxy
- /admin/registry (GET, POST): List/Upsert registry (admin only)
- /admin/registry/{provider} (GET, DELETE): Get/Delete registry (admin only)

Quick start:
- Copy .env.example to .env and set values (do not commit secrets).
- Install dependencies: pip install -r requirements.txt
- Run: uvicorn src.api.main:app --host 0.0.0.0 --port 3001
- Docs: http://localhost:3001/docs

Notes:
- Current implementation uses in-memory stores as stubs. Replace with a real database.
- Rate limiting is in-memory and per-process; consider a distributed limiter for production.
- Admin endpoints require header: X-API-Key: <ADMIN_API_KEY>.
