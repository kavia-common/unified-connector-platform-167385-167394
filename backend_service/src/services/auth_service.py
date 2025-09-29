"""
Authentication service orchestrating API-key and OAuth flows.
"""

from __future__ import annotations
import secrets
from typing import List, Optional, Tuple

from src.services.database import store_token
from src.services.external_providers import (
    build_oauth_authorization_url,
    exchange_code_for_token,
    verify_api_key,
)


# PUBLIC_INTERFACE
def handle_api_key_auth(tenant_id: str, provider: str, api_key: str, label: Optional[str]) -> str:
    """
    Validate API key with provider (stub) and store token.
    Returns token_id.
    """
    if not verify_api_key(provider, api_key):
        raise ValueError("Invalid API key")
    token_id = store_token(tenant_id=tenant_id, provider=provider, secret=api_key, meta={"label": label})
    return token_id


# PUBLIC_INTERFACE
def initiate_oauth(tenant_id: str, provider: str, redirect_base: str, redirect_path: str, scope: Optional[List[str]], state: Optional[str]) -> Tuple[str, str]:
    """
    Build authorization URL and state. Returns (auth_url, state).
    """
    final_state = state or secrets.token_urlsafe(16)
    redirect_uri = f"{redirect_base.rstrip('/')}{redirect_path}"
    auth_url = build_oauth_authorization_url(provider=provider, redirect_uri=redirect_uri, scope=scope, state=final_state)
    return auth_url, final_state


# PUBLIC_INTERFACE
def complete_oauth_callback(tenant_id: str, provider: str, code: str, redirect_base: str, redirect_path: str, state: str) -> str:
    """
    Exchange code for token and store it. Returns token_id.
    """
    redirect_uri = f"{redirect_base.rstrip('/')}{redirect_path}"
    access_token, meta = exchange_code_for_token(provider=provider, code=code, redirect_uri=redirect_uri)
    token_id = store_token(tenant_id=tenant_id, provider=provider, secret=access_token, meta={"oauth": True, **meta})
    return token_id
