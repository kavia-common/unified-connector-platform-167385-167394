"""
Pydantic models (schemas) for request and response bodies.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, HttpUrl


# Shared
class TenantContext(BaseModel):
    """Represents the tenant context for operations."""
    tenant_id: str = Field(..., description="Unique identifier of the tenant")


class ProviderAuthMethod(str):
    """Enum-like for provider auth method values."""
    API_KEY = "api_key"
    OAUTH = "oauth"


# Authentication
class APIKeyAuthRequest(TenantContext):
    provider: str = Field(..., description="Provider name (e.g., jira, confluence)")
    api_key: str = Field(..., min_length=1, description="API key for the provider")
    label: Optional[str] = Field(default=None, description="Optional label for this key")


class APIKeyAuthResponse(BaseModel):
    message: str = Field(..., description="Result message")
    provider: str = Field(..., description="Provider name")
    tenant_id: str = Field(..., description="Tenant")
    token_id: str = Field(..., description="Reference ID of stored token")


class OAuthInitRequest(TenantContext):
    provider: str = Field(..., description="Provider name")
    redirect_path: Optional[str] = Field(
        default="/oauth/callback", description="Path on SITE_URL for callback"
    )
    scope: Optional[List[str]] = Field(default=None, description="Optional scopes list")
    state: Optional[str] = Field(default=None, description="Optional opaque state")


class OAuthInitResponse(BaseModel):
    authorization_url: HttpUrl = Field(..., description="Provider authorization URL")
    state: str = Field(..., description="State for CSRF protection")


class OAuthCallbackRequest(BaseModel):
    tenant_id: str = Field(..., description="Tenant")
    provider: str = Field(..., description="Provider")
    code: str = Field(..., description="Authorization code from provider")
    state: str = Field(..., description="State used in initiation")


class OAuthCallbackResponse(BaseModel):
    message: str = Field(..., description="Result")
    provider: str = Field(..., description="Provider")
    tenant_id: str = Field(..., description="Tenant")
    token_id: str = Field(..., description="Stored token reference")


# Connectors
class ConnectorBase(BaseModel):
    provider: str = Field(..., description="Provider name (e.g., jira)")
    auth_method: str = Field(..., description="Auth method: api_key or oauth")
    label: Optional[str] = Field(default=None, description="Optional connector label")
    config: Dict[str, Any] = Field(default_factory=dict, description="Provider config")


class ConnectorCreateRequest(TenantContext, ConnectorBase):
    pass


class ConnectorUpdateRequest(BaseModel):
    label: Optional[str] = Field(default=None, description="Label")
    config: Optional[Dict[str, Any]] = Field(default=None, description="Config")


class ConnectorResponse(ConnectorBase):
    id: str = Field(..., description="Connector unique identifier")
    tenant_id: str = Field(..., description="Tenant")
    status: str = Field(..., description="Connection status (e.g., connected, error)")


class ConnectorListResponse(BaseModel):
    items: List[ConnectorResponse] = Field(..., description="List of connectors")
    total: int = Field(..., description="Total count")


# LLM Proxy
class LLMToolInvocation(BaseModel):
    tool: str = Field(..., description="Tool name (e.g., search_projects)")
    provider: str = Field(..., description="Provider name")
    tenant_id: str = Field(..., description="Tenant")
    connector_id: Optional[str] = Field(
        default=None, description="Optional connector to use"
    )
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Tool args")


class LLMToolResponse(BaseModel):
    provider: str = Field(..., description="Provider")
    tool: str = Field(..., description="Tool invoked")
    result: Any = Field(..., description="Result payload")


# Registry (Admin)
class RegistryConnector(BaseModel):
    provider: str = Field(..., description="Provider")
    display_name: str = Field(..., description="Display name")
    auth_methods: List[str] = Field(..., description="Supported auth methods")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Extra metadata")


class RegistryUpsertRequest(RegistryConnector):
    pass


class RegistryListResponse(BaseModel):
    items: List[RegistryConnector] = Field(..., description="Registered connectors")
    total: int = Field(..., description="Total count")
