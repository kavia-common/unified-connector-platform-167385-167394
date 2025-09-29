"""
OpenAPI utilities and tags for the Unified Connector Platform API.
"""

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi as _get_openapi

openapi_tags = [
    {
        "name": "Authentication",
        "description": "Authentication flows including API key and OAuth.",
    },
    {
        "name": "Connectors",
        "description": "CRUD operations and management of connectors per tenant.",
    },
    {
        "name": "LLM Proxy",
        "description": "Proxy LLM requests to provider tools safely.",
    },
    {
        "name": "Admin - Registry",
        "description": "Admin-only endpoints to manage connector registry.",
    },
    {
        "name": "Documentation",
        "description": "Documentation helper endpoints.",
    },
]


def get_openapi_schema(app: FastAPI):
    """
    Build and memoize the OpenAPI schema with custom metadata.

    Note:
        Use getattr to safely access app.openapi_schema; directly referencing it
        before initialization can raise AttributeError and break /openapi.json and /docs.
    """
    # Safely check cached schema
    cached = getattr(app, "openapi_schema", None)
    if cached:
        return cached

    # Generate new schema
    openapi_schema = _get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Cache and return
    app.openapi_schema = openapi_schema
    return app.openapi_schema
