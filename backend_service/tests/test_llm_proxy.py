def test_llm_proxy_basic_invocation_without_connector(client):
    payload = {
        "provider": "jira",
        "tool": "search_projects",
        "tenant_id": "t-1",
        "arguments": {"q": "demo"},
    }
    resp = client.post("/llm-proxy", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["provider"] == "jira"
    assert data["tool"] == "search_projects"
    # Result shape
    result = data["result"]
    assert isinstance(result, dict)
    assert result.get("provider") == "jira"
    assert result.get("tool") == "search_projects"
    assert result.get("used_token") in (True, False)
    # Since no connector provided, token should be unused
    assert result.get("used_token") is False
