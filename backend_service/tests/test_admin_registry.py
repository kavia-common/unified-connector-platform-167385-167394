def test_registry_requires_admin_key(client):
    # Missing key
    resp = client.get("/admin/registry")
    assert resp.status_code in (401, 403, 422) or resp.status_code == 401
    # Wrong key
    resp = client.get("/admin/registry", headers={"X-API-Key": "wrong"})
    assert resp.status_code == 401


def test_registry_crud_with_admin_key(client, admin_headers):
    # List initially
    resp = client.get("/admin/registry", headers=admin_headers)
    assert resp.status_code == 200
    initial = resp.json()
    assert "items" in initial and "total" in initial

    item = {
        "provider": "jira",
        "display_name": "Jira",
        "auth_methods": ["api_key", "oauth"],
        "metadata": {"docs": "https://example.com"},
    }
    # Upsert
    resp = client.post("/admin/registry", headers=admin_headers, json=item)
    assert resp.status_code == 200
    saved = resp.json()
    assert saved["provider"] == "jira"
    assert saved["display_name"] == "Jira"

    # Get by provider
    resp = client.get("/admin/registry/jira", headers=admin_headers)
    assert resp.status_code == 200
    got = resp.json()
    assert got["provider"] == "jira"

    # List should include our item
    resp = client.get("/admin/registry", headers=admin_headers)
    assert resp.status_code == 200
    listed = resp.json()
    assert any(i["provider"] == "jira" for i in listed["items"])

    # Delete
    resp = client.delete("/admin/registry/jira", headers=admin_headers)
    assert resp.status_code == 200
    assert resp.json()["message"] == "deleted"
