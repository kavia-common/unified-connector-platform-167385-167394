"""
Registry service for managing enabled providers and their metadata.
"""

from __future__ import annotations
from typing import Dict, List

from src.services.database import (
    delete_registry_item,
    get_registry,
    get_registry_item,
    upsert_registry_item,
)


# PUBLIC_INTERFACE
def list_registry_items() -> List[Dict]:
    """List all registry items."""
    return get_registry()


# PUBLIC_INTERFACE
def upsert_registry_entry(item: Dict) -> Dict:
    """Create or update a registry entry."""
    return upsert_registry_item(item)


# PUBLIC_INTERFACE
def remove_registry_entry(provider: str) -> bool:
    """Remove a registry entry."""
    return delete_registry_item(provider)


# PUBLIC_INTERFACE
def get_registry_entry(provider: str) -> Dict | None:
    """Get a registry entry."""
    return get_registry_item(provider)
