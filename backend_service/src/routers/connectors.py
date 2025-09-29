"""
Connectors router providing CRUD operations for connectors.
"""

from __future__ import annotations
from fastapi import APIRouter, Query

from src.core.errors import NotFoundError
from src.models.schemas import (
    ConnectorCreateRequest,
    ConnectorListResponse,
    ConnectorResponse,
    ConnectorUpdateRequest,
)
from src.services.connectors_service import (
    create_connector_record,
    delete_connector_record,
    get_connector_record,
    list_connector_records,
    update_connector_record,
)

router = APIRouter()


@router.get(
    "",
    summary="List connectors",
    response_model=ConnectorListResponse,
)
def list_connectors(tenant_id: str | None = Query(default=None, description="Filter by tenant_id")):
    """
    List connectors. Optionally filter by tenant_id.
    """
    items = [ConnectorResponse(**c) for c in list_connector_records(tenant_id=tenant_id)]
    return ConnectorListResponse(items=items, total=len(items))


@router.post(
    "",
    summary="Create connector",
    response_model=ConnectorResponse,
)
def create_connector(payload: ConnectorCreateRequest):
    """
    Create a connector record. Attach token_id if already stored for this tenant/provider via a previous auth flow (out of scope for this stub).
    """
    # In a real implementation, we would look up a default token for tenant/provider.
    record = create_connector_record(
        tenant_id=payload.tenant_id,
        provider=payload.provider,
        auth_method=payload.auth_method,
        label=payload.label,
        config=payload.config,
        token_id=None,  # Associate later or via dedicated endpoint
    )
    return ConnectorResponse(**record)


@router.get(
    "/{connector_id}",
    summary="Get connector",
    response_model=ConnectorResponse,
    responses={404: {"description": "Not Found"}},
)
def get_connector(connector_id: str):
    """
    Get a connector by ID.
    """
    record = get_connector_record(connector_id)
    if not record:
        raise NotFoundError("Connector not found")
    return ConnectorResponse(**record)


@router.patch(
    "/{connector_id}",
    summary="Update connector",
    response_model=ConnectorResponse,
)
def update_connector(connector_id: str, payload: ConnectorUpdateRequest):
    """
    Update connector label/config.
    """
    updates = {}
    if payload.label is not None:
        updates["label"] = payload.label
    if payload.config is not None:
        updates["config"] = payload.config
    record = update_connector_record(connector_id, updates)
    if not record:
        raise NotFoundError("Connector not found")
    return ConnectorResponse(**record)


@router.delete(
    "/{connector_id}",
    summary="Delete connector",
    response_model=dict,
)
def delete_connector(connector_id: str):
    """
    Delete a connector by ID.
    """
    ok = delete_connector_record(connector_id)
    if not ok:
        raise NotFoundError("Connector not found")
    return {"message": "deleted", "id": connector_id}
