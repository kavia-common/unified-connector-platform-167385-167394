from urllib.parse import urlparse, parse_qs

def test_oauth_init_returns_url_and_state(client):
    payload = {"tenant_id": "t-1", "provider": "jira", "redirect_path": "/oauth/callback"}
    resp = client.post("/auth/oauth/init", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "authorization_url" in data and "state" in data
    # Validate URL contains expected query params
    parsed = urlparse(data["authorization_url"])
    assert parsed.scheme in ("http", "https")
    qs = parse_qs(parsed.query)
    assert "redirect_uri" in qs
    assert "state" in qs
    assert "client_id" in qs


def test_oauth_callback_returns_token_id(client):
    # We can simulate a callback regardless of the state linkage in this stub
    payload = {
        "tenant_id": "t-1",
        "provider": "jira",
        "code": "abc123",
        "state": "some-state",
    }
    resp = client.post("/auth/oauth/callback", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["message"] == "OAuth token stored"
    assert data["provider"] == "jira"
    assert data["tenant_id"] == "t-1"
    assert isinstance(data["token_id"], str) and data["token_id"]
