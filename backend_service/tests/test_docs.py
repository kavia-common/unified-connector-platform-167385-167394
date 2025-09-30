def test_docs_ui_available(client):
    resp = client.get("/docs")
    assert resp.status_code == 200
    # Swagger UI HTML should contain references to Swagger UI
    text = resp.text.lower()
    assert "swagger" in text and ("swagger ui" in text or "swagger-ui" in text)


def test_openapi_json_served(client):
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    data = resp.json()
    assert "openapi" in data
    assert "paths" in data
    # Check presence of key endpoints in the spec
    for path in ["/auth/api-key", "/auth/oauth/init", "/connectors", "/llm-proxy", "/admin/registry"]:
        assert path in data["paths"]
