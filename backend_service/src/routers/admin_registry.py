"""
Admin registry router for managing available providers and their metadata.
"""

from __future__ import annotations
from typing import Optional

from fastapi import APIRouter, Depends, Header

from src.core.config import get_settings
from src.core.errors import NotFoundError, UnauthorizedError
from src.models.schemas import RegistryListResponse, RegistryUpsertRequest, RegistryConnector
from src.services.registry_service import (
    get_registry_entry,
    list_registry_items,
    remove_registry_entry,
    upsert_registry_entry,
)

router = APIRouter()


def require_admin(x_api_key: Optional[str] = Header(default=None, alias="X-API-Key")):
    """
    Simple admin guard using header X-API-Key.
    """
    settings = get_settings()
    if not x_api_key or x_api_key != settings.ADMIN_API_KEY:
        raise UnauthorizedError("Admin API key invalid")
    return True


@router.get(
    "",
    summary="List registry providers",
    response_model=RegistryListResponse,
    dependencies=[Depends(require_admin)],
)
def list_registry():
    """
    List all providers in the registry.
    """
    items = [RegistryConnector(**i) for i in list_registry_items()]
    return RegistryListResponse(items=items, total=len(items))


@router.post(
    "",
    summary="Upsert registry provider",
    response_model=RegistryConnector,
    dependencies=[Depends(require_admin)],
)
def upsert_registry(payload: RegistryUpsertRequest):
    """
    Create or update a provider registry entry.
    """
    saved = upsert_registry_entry(payload.model_dump())
    return RegistryConnector(**saved)


@router.get(
    "/{provider}",
    summary="Get registry provider",
    response_model=RegistryConnector,
    dependencies=[Depends(require_admin)],
)
def get_registry_provider(provider: str):
    """
    Get a specific provider registry entry.
    """
    item = get_registry_entry(provider)
    if not item:
        raise NotFoundError("Provider registry entry not found")
    return RegistryConnector(**item)


@router.delete(
    "/{provider}",
    summary="Delete registry provider",
    response_model=dict,
    dependencies=[Depends(require_admin)],
)
def delete_registry_provider(provider: str):
    """
    Delete a provider registry entry.
    """
    ok = remove_registry_entry(provider)
    if not ok:
        raise NotFoundError("Provider registry entry not found")
    return {"message": "deleted", "provider": provider}
