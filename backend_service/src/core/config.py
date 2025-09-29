"""
Application settings and configuration.
"""

import os
from functools import lru_cache
from typing import List, Callable

from pydantic import BaseModel, Field


class Settings(BaseModel):
    """
    Settings loaded from environment variables.

    Note: The orchestrator will provision actual values into .env.
    """

    ENV: str = Field(default=os.getenv("ENV", "development"), description="Environment")
    CORS_ALLOW_ORIGINS: List[str] = Field(
        default_factory=lambda: os.getenv("CORS_ALLOW_ORIGINS", "*").split(","),
        description="Allowed CORS origins",
    )

    # Rate limiting
    RATE_LIMIT_REQUESTS: int = Field(
        default=int(os.getenv("RATE_LIMIT_REQUESTS", "100")), description="Requests"
    )
    RATE_LIMIT_WINDOW_SECONDS: int = Field(
        default=int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60")),
        description="Window size in seconds",
    )

    # OAuth callback base URL
    SITE_URL: str = Field(
        default=os.getenv("SITE_URL", "http://localhost:3001"),
        description="Base site URL for OAuth redirects",
    )

    # Token encryption key placeholder (for future use)
    TOKEN_ENCRYPTION_KEY: str = Field(
        default=os.getenv("TOKEN_ENCRYPTION_KEY", "dev-not-secure"),
        description="Key for encrypting stored tokens (use KMS/Vault in prod)",
    )

    # ADMIN API KEY for registry endpoints (simple auth guard)
    ADMIN_API_KEY: str = Field(
        default=os.getenv("ADMIN_API_KEY", "change-me"),
        description="Admin API key for privileged endpoints",
    )

    def rate_limit_key_func(self) -> Callable[[dict], str]:
        """
        Returns a function that extracts a rate limit key from request scope.
        Defaults to client host (IP). In real-world, prefer user/tenant ID from auth.
        """

        def key_func(scope: dict) -> str:
            client = scope.get("client")
            try:
                host = client[0] if client and isinstance(client, (tuple, list)) and len(client) > 0 else "unknown"
            except Exception:
                host = "unknown"
            return f"ip:{host}"

        return key_func


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Returns cached application settings.
    """
    return Settings()
