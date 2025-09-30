"""
Pseudo end-to-end test simulating an authentic user flow:
1) Authenticate by creating an API key (POST /auth/api-key)
2) Add a new connector (POST /connectors) and verify status
3) Use the connector to fetch a resource via /llm-proxy (e.g., 'search_projects' for Jira)
4) Assert that the response is 200 and contains expected result structure

This test intentionally uses the public HTTP endpoints and the TestClient
to mimic end-to-end behavior through the FastAPI app stack.

Note:
- The implementation uses in-memory stubs, so the "external" calls are simulated.
- We leverage the environment setup from tests/conftest.py
"""

from typing import Dict


def test_pseudo_e2e_auth_create_connector_invoke_tool(client):
    # 1) Authenticate by creating an API key
    tenant_id = "tenant-e2e-1"
    provider = "jira"
    api_key_payload = {
        "tenant_id": tenant_id,
        "provider": provider,
        "api_key": "e2e-secret-key",
        "label": "e2e-primary",
    }
    auth_resp = client.post("/auth/api-key", json=api_key_payload)
    assert auth_resp.status_code == 200, auth_resp.text
    auth_data = auth_resp.json()
    assert auth_data["message"] == "API key stored"
    assert auth_data["provider"] == provider
    assert auth_data["tenant_id"] == tenant_id
    assert isinstance(auth_data["token_id"], str) and auth_data["token_id"]

    # 2) Add a new connector and verify its response schema
    connector_payload: Dict = {
        "tenant_id": tenant_id,
        "provider": provider,
        "auth_method": "api_key",
        "label": "e2e-connector",
        "config": {"site": "example.atlassian.net"},
    }
    conn_resp = client.post("/connectors", json=connector_payload)
    assert conn_resp.status_code == 200, conn_resp.text
    connector = conn_resp.json()
    assert connector["tenant_id"] == tenant_id
    assert connector["provider"] == provider
    assert connector["auth_method"] == "api_key"
    assert isinstance(connector["id"], str) and connector["id"]
    # With current stub, connector without token_id defaults to 'pending'
    # We check that status field exists and is a valid string
    assert isinstance(connector.get("status"), str)
    connector_id = connector["id"]

    # 3) Use the connector to fetch a resource via /llm-proxy
    # Even if the connector has no token associated in the stub, the proxy layer
    # will still return a structured mock result. We still provide the connector_id
    # to simulate a realistic call path.
    tool_payload = {
        "provider": provider,
        "tool": "search_projects",
        "tenant_id": tenant_id,
        "connector_id": connector_id,
        "arguments": {"q": "demo"},
    }
    proxy_resp = client.post("/llm-proxy", json=tool_payload)
    assert proxy_resp.status_code == 200, proxy_resp.text
    data = proxy_resp.json()

    # 4) Assert expected result structure
    assert data["provider"] == provider
    assert data["tool"] == "search_projects"
    result = data.get("result")
    assert isinstance(result, dict)
    # The stub returns a shape with these keys
    assert result.get("provider") == provider
    assert result.get("tool") == "search_projects"
    assert "args" in result and isinstance(result["args"], dict)
    assert "used_token" in result and result["used_token"] in (True, False)
    # The stub includes a 'data' array payload with objects
    assert "data" in result and isinstance(result["data"], list)
    if result["data"]:
        first = result["data"][0]
        assert isinstance(first, dict)
        assert "id" in first and "name" in first
