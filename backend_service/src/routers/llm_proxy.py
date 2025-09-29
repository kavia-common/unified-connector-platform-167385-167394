"""
LLM Proxy router for tool invocations through provider connectors.
"""

from __future__ import annotations

from fastapi import APIRouter

from src.models.schemas import LLMToolInvocation, LLMToolResponse
from src.services.llm_proxy_service import proxy_llm_tool

router = APIRouter()


@router.post(
    "",
    summary="Invoke LLM Tool",
    response_model=LLMToolResponse,
    responses={400: {"description": "Bad Request"}},
)
def invoke_tool(payload: LLMToolInvocation):
    """
    Invoke a provider tool through the unified proxy.

    Parameters:
    - provider: Target provider
    - tool: Tool name (e.g., search_projects)
    - tenant_id: Tenant context
    - connector_id: Optional connector ID to use
    - arguments: Tool arguments

    Returns:
    - Tool result payload
    """
    result = proxy_llm_tool(
        provider=payload.provider,
        tool=payload.tool,
        connector_id=payload.connector_id,
        args=payload.arguments,
    )
    return LLMToolResponse(provider=payload.provider, tool=payload.tool, result=result)
