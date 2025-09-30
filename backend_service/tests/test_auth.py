def test_auth_api_key_success(client):
    payload = {
        "tenant_id": "t-1",
        "provider": "jira",
        "api_key": "secret-key",
        "label": "primary",
    }
    resp = client.post("/auth/api-key", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["message"] == "API key stored"
    assert data["provider"] == "jira"
    assert data["tenant_id"] == "t-1"
    assert isinstance(data["token_id"], str) and len(data["token_id"]) > 0


def test_auth_api_key_validation_error(client):
    # Missing required api_key -> 422 validation error
    payload = {
        "tenant_id": "t-1",
        "provider": "jira",
    }
    resp = client.post("/auth/api-key", json=payload)
    assert resp.status_code == 422
