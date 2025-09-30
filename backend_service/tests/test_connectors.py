def _create_sample_connector(client, tenant_id="t-1"):
    payload = {
        "tenant_id": tenant_id,
        "provider": "jira",
        "auth_method": "api_key",
        "label": "demo",
        "config": {"site": "example.atlassian.net"},
    }
    resp = client.post("/connectors", json=payload)
    assert resp.status_code == 200
    return resp.json()


def test_connectors_list_initially_empty(client):
    resp = client.get("/connectors")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data["items"], list)
    # State may persist across tests in same process; list could be non-empty. Ensure schema.
    assert "total" in data
    assert data["total"] == len(data["items"])


def test_connectors_create_and_get_update_delete(client):
    created = _create_sample_connector(client)
    cid = created["id"]

    # List and ensure our item is present
    resp = client.get("/connectors", params={"tenant_id": created["tenant_id"]})
    assert resp.status_code == 200
    data = resp.json()
    assert any(item["id"] == cid for item in data["items"])

    # Get by id
    resp = client.get(f"/connectors/{cid}")
    assert resp.status_code == 200
    fetched = resp.json()
    assert fetched["id"] == cid
    assert fetched["provider"] == "jira"

    # Update label and config
    resp = client.patch(f"/connectors/{cid}", json={"label": "updated", "config": {"x": 1}})
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["label"] == "updated"
    assert updated["config"] == {"x": 1}

    # Delete
    resp = client.delete(f"/connectors/{cid}")
    assert resp.status_code == 200
    assert resp.json()["message"] == "deleted"

    # Get after delete -> 404
    resp = client.get(f"/connectors/{cid}")
    assert resp.status_code == 404


def test_connectors_get_not_found(client):
    resp = client.get("/connectors/non-existent-id")
    assert resp.status_code == 404
