import os
import pytest
from fastapi.testclient import TestClient

# Ensure ENV is development for richer error payloads during tests
@pytest.fixture(autouse=True)
def _set_test_env(monkeypatch):
    monkeypatch.setenv("ENV", "development")
    # Provide a predictable admin key for protected endpoints
    monkeypatch.setenv("ADMIN_API_KEY", "test-admin-key")
    # Set a site URL to validate OAuth redirects
    monkeypatch.setenv("SITE_URL", "http://testserver")
    yield


@pytest.fixture(scope="session")
def app():
    # Import here to ensure dotenv, settings loading, and router wiring are executed
    from src.api.main import create_app
    return create_app()


@pytest.fixture()
def client(app):
    # FastAPI TestClient uses Starlette test client underneath
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def admin_headers():
    return {"X-API-Key": os.getenv("ADMIN_API_KEY", "test-admin-key")}
