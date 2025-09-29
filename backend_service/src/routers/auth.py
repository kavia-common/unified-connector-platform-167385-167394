"""
Authentication router handling API-key and OAuth flows.
"""

from __future__ import annotations

from fastapi import APIRouter
from src.core.config import get_settings
from src.core.errors import AppError
from src.models.schemas import (
    APIKeyAuthRequest,
    APIKeyAuthResponse,
    OAuthCallbackRequest,
    OAuthCallbackResponse,
    OAuthInitRequest,
    OAuthInitResponse,
)
from src.services.auth_service import (
    complete_oauth_callback,
    handle_api_key_auth,
    initiate_oauth,
)

router = APIRouter()


@router.post(
    "/api-key",
    summary="Authenticate with API Key",
    response_model=APIKeyAuthResponse,
    responses={400: {"description": "Bad Request"}, 401: {"description": "Unauthorized"}},
)
def auth_api_key(payload: APIKeyAuthRequest):
    """
    Authenticate a tenant with a provider using API key.

    Parameters:
    - tenant_id: Tenant performing authentication
    - provider: Provider name
    - api_key: Provider API key
    - label: Optional label for token

    Returns:
    - token_id referencing the stored token
    """
    try:
        token_id = handle_api_key_auth(
            tenant_id=payload.tenant_id,
            provider=payload.provider,
            api_key=payload.api_key,
            label=payload.label,
        )
        return APIKeyAuthResponse(
            message="API key stored",
            provider=payload.provider,
            tenant_id=payload.tenant_id,
            token_id=token_id,
        )
    except ValueError as e:
        raise AppError(detail=str(e), code="invalid_credentials", status_code=401)


@router.post(
    "/oauth/init",
    summary="Initiate OAuth flow",
    response_model=OAuthInitResponse,
)
def oauth_init(payload: OAuthInitRequest):
    """
    Initiate an OAuth flow for a provider.

    The response contains an authorization_url and a state value.
    The client should redirect the user-agent to the authorization_url.
    """
    settings = get_settings()
    auth_url, state = initiate_oauth(
        tenant_id=payload.tenant_id,
        provider=payload.provider,
        redirect_base=settings.SITE_URL,
        redirect_path=payload.redirect_path or "/oauth/callback",
        scope=payload.scope,
        state=payload.state,
    )
    return OAuthInitResponse(authorization_url=auth_url, state=state)


@router.post(
    "/oauth/callback",
    summary="Complete OAuth callback",
    response_model=OAuthCallbackResponse,
)
def oauth_callback(payload: OAuthCallbackRequest):
    """
    Complete OAuth flow by exchanging authorization code for an access token.

    Parameters:
    - tenant_id, provider, code, state

    Returns:
    - token_id referencing the stored token
    """
    settings = get_settings()
    token_id = complete_oauth_callback(
        tenant_id=payload.tenant_id,
        provider=payload.provider,
        code=payload.code,
        redirect_base=settings.SITE_URL,
        redirect_path="/oauth/callback",
        state=payload.state,
    )
    return OAuthCallbackResponse(
        message="OAuth token stored",
        provider=payload.provider,
        tenant_id=payload.tenant_id,
        token_id=token_id,
    )
