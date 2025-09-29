"""
LLM proxy service that routes tool invocations to providers using connector tokens.
"""

from __future__ import annotations
from typing import Any, Dict, Optional

from src.services.database import get_token_by_connector
from src.services.external_providers import invoke_llm_tool


# PUBLIC_INTERFACE
def proxy_llm_tool(provider: str, tool: str, connector_id: Optional[str], args: Dict[str, Any]) -> Any:
    """
    Proxy a tool call to the provider through the configured connector token if provided.
    """
    token_secret: str | None = None
    if connector_id:
        token = get_token_by_connector(connector_id)
        if token:
            token_secret = token.get("secret")

    result = invoke_llm_tool(provider=provider, tool=tool, token_secret=token_secret, args=args)
    return result
