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

Backend base URL:
- By default this service listens on http://localhost:3001
- Ensure your frontend points to http://localhost:3001 for API calls (e.g., NEXT_PUBLIC_BACKEND_URL=http://localhost:3001).
- A 404 Not Found from the frontend for POST /auth/api-key usually indicates the frontend is targeting the wrong port or path (e.g., 4000). Verify the base URL matches the running FastAPI server.

CORS configuration:
- CORS is enabled with CORSMiddleware and controlled via the CORS_ALLOW_ORIGINS environment variable (comma-separated list or "*" for all in development).
- Set CORS_ALLOW_ORIGINS to your frontend origin(s), e.g., http://localhost:3000.

OAuth redirect_uri configuration (important):
- The backend constructs redirect_uri as: `${SITE_URL}${redirect_path}` where:
  - SITE_URL comes from the environment (Settings.SITE_URL).
  - redirect_path defaults to `/oauth/callback` (frontend passes this explicitly).
- To avoid OAuth errors, Jira's application link redirect URL must exactly match:
  - Protocol, host (and port), and path.
- Example for this environment:
  - If backend is reachable at: https://vscode-internal-32364-beta.beta01.cloud.kavia.ai:3001
  - Set: SITE_URL=https://vscode-internal-32364-beta.beta01.cloud.kavia.ai:3001
  - Then redirect_uri becomes: https://vscode-internal-32364-beta.beta01.cloud.kavia.ai:3001/oauth/callback
  - Register exactly that URL in Jira.

Testing POST /auth/api-key:
- Example curl:
  curl -X POST "http://localhost:3001/auth/api-key" \
    -H "Content-Type: application/json" \
    -d '{"tenant_id":"t-1","provider":"jira","api_key":"secret","label":"primary"}'
- You should receive 200 OK with a token_id. If you see 404, confirm:
  1) The server is running on port 3001.
  2) You used the correct path: /auth/api-key.
  3) Any proxy in front is forwarding correctly.

Notes:
- Current implementation uses in-memory stores as stubs. Replace with a real database.
- Rate limiting is in-memory and per-process; consider a distributed limiter for production.
- Admin endpoints require header: X-API-Key: <ADMIN_API_KEY>.
