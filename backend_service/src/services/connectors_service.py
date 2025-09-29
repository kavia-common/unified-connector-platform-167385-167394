"""
Connectors service for CRUD operations and token association.
"""

from __future__ import annotations
from typing import Any, Dict, List

from src.services.database import (
    create_connector,
    delete_connector,
    get_connector,
    list_connectors,
    update_connector,
)


# PUBLIC_INTERFACE
def create_connector_record(
    tenant_id: str,
    provider: str,
    auth_method: str,
    label: str | None,
    config: Dict[str, Any],
    token_id: str | None,
) -> Dict[str, Any]:
    """Create and return a connector record."""
    return create_connector(
        tenant_id=tenant_id,
        provider=provider,
        auth_method=auth_method,
        label=label,
        config=config,
        token_id=token_id,
    )


# PUBLIC_INTERFACE
def list_connector_records(tenant_id: str | None = None) -> List[Dict[str, Any]]:
    """List connectors, optionally filtered by tenant."""
    return list_connectors(tenant_id=tenant_id)


# PUBLIC_INTERFACE
def get_connector_record(connector_id: str) -> Dict[str, Any] | None:
    """Get a single connector."""
    return get_connector(connector_id)


# PUBLIC_INTERFACE
def update_connector_record(connector_id: str, updates: Dict[str, Any]) -> Dict[str, Any] | None:
    """Update a connector."""
    return update_connector(connector_id, updates)


# PUBLIC_INTERFACE
def delete_connector_record(connector_id: str) -> bool:
    """Delete a connector."""
    return delete_connector(connector_id)
