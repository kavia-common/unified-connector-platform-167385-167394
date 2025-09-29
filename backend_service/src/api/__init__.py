"""
API package initializer for the Unified Connector Platform backend.

Exposes helpers to retrieve the FastAPI app or its factory.
"""

# PUBLIC_INTERFACE
def get_app():
    """Return the FastAPI application instance."""
    from .main import app
    return app


# PUBLIC_INTERFACE
def get_app_factory():
    """Return the FastAPI application factory callable."""
    from .main import create_app
    return create_app
