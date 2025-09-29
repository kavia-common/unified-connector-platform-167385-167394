"""
FastAPI backend for the Unified Connector Platform.

This application exposes REST endpoints for:
- /auth/api-key: API-key based authentication flows
- /auth/oauth: OAuth flows (initiation, callback)
- /connectors: CRUD management of connectors per tenant
- /llm-proxy: LLM tools proxy to external providers
- /admin/registry: Admin management of connector registry

It includes:
- Modular routers organized by domain
- Pydantic models with strict validation
- Error handling with consistent response format
- Basic rate limiting middleware (in-memory token bucket)
- Token management stubs per tenant/provider
- External provider and database stubs for future integration
- OpenAPI metadata and tags
- CORS and security considerations

Environment configuration:
- Do not hardcode secrets. Expect values from environment variables.
- You may create .env.example to document required variables.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import get_settings
from src.core.errors import register_exception_handlers
from src.core.rate_limit import RateLimitMiddleware
from src.routers.auth import router as auth_router
from src.routers.connectors import router as connectors_router
from src.routers.llm_proxy import router as llm_proxy_router
from src.routers.admin_registry import router as admin_registry_router
from src.core.openapi import get_openapi_schema, openapi_tags


# PUBLIC_INTERFACE
def create_app() -> FastAPI:
    """
    Factory to create a configured FastAPI application instance.

    Returns:
        FastAPI: Configured app instance with routers, middleware, and docs.
    """
    settings = get_settings()
    app = FastAPI(
        title="Unified Connector Platform API",
        description=(
            "A unified API to authenticate, connect, and interact with third-party providers "
            "(e.g., Jira, Confluence) via API Key or OAuth, manage connectors per tenant, "
            "operate on provider resources, leverage LLM tools proxy, and manage a connector registry."
        ),
        version="1.0.0",
        openapi_tags=openapi_tags,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Rate limiting middleware (simple in-memory)
    app.add_middleware(
        RateLimitMiddleware,
        requests=settings.RATE_LIMIT_REQUESTS,
        window_seconds=settings.RATE_LIMIT_WINDOW_SECONDS,
        key_func=settings.rate_limit_key_func,
    )

    # Register exception handlers
    register_exception_handlers(app)

    # Routers
    app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
    app.include_router(connectors_router, prefix="/connectors", tags=["Connectors"])
    app.include_router(llm_proxy_router, prefix="/llm-proxy", tags=["LLM Proxy"])
    app.include_router(
        admin_registry_router, prefix="/admin/registry", tags=["Admin - Registry"]
    )

    @app.get("/", summary="Health Check")
    def health_check():
        """
        Health check endpoint.
        Returns status and version info.
        """
        return {"status": "ok", "service": "backend_service", "version": app.version}

    @app.get(
        "/docs/websocket-usage",
        summary="WebSocket Usage",
        description="This project currently exposes only HTTP endpoints. If WebSocket endpoints are added, usage notes will appear here.",
        tags=["Documentation"],
    )
    def websocket_usage():
        """
        WebSocket usage documentation endpoint.
        """
        return {"message": "No WebSocket endpoints available at this time."}

    # Replace default openapi generator to include custom metadata
    app.openapi = lambda: get_openapi_schema(app)

    return app


# PUBLIC_INTERFACE
app = create_app()
