"""
External provider API integration stubs.

Replace these with concrete HTTP calls to provider APIs (e.g., Jira, Confluence).
"""

from __future__ import annotations
from typing import Any, Dict, List, Tuple
from urllib.parse import urlencode




# PUBLIC_INTERFACE
def build_oauth_authorization_url(provider: str, redirect_uri: str, scope: List[str] | None, state: str) -> str:
    """Build a mock authorization URL."""
    base = f"https://auth.{provider}.example.com/authorize"
    params = {
        "response_type": "code",
        "client_id": f"{provider}-mock-client-id",
        "redirect_uri": redirect_uri,
        "scope": " ".join(scope or ["basic"]),
        "state": state,
    }
    return f"{base}?{urlencode(params)}"


# PUBLIC_INTERFACE
def exchange_code_for_token(provider: str, code: str, redirect_uri: str) -> Tuple[str, Dict[str, Any]]:
    """
    Exchange auth code for token (stub).
    Returns (access_token, meta).
    """
    access_token = f"{provider}-access-{code}"
    meta = {"expires_in": 3600}
    return access_token, meta


# PUBLIC_INTERFACE
def verify_api_key(provider: str, api_key: str) -> bool:
    """
    Verify API key with provider (stub).
    Always returns True in this stub.
    """
    return True


# PUBLIC_INTERFACE
def invoke_llm_tool(provider: str, tool: str, token_secret: str | None, args: Dict[str, Any]) -> Any:
    """
    Invoke provider-specific tool (stub).
    """
    # Simulate result payload
    return {
        "provider": provider,
        "tool": tool,
        "args": args,
        "used_token": bool(token_secret),
        "data": [{"id": "sample-1", "name": "Example"}],
    }
