"""
Error types and handlers for consistent API responses.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uuid
from src.core.config import get_settings


class ErrorResponse(BaseModel):
    """Standard error response model."""
    detail: str = Field(..., description="Human-readable error detail")
    code: str | None = Field(default=None, description="Machine-readable error code")


class AppError(Exception):
    """Base application error."""
    def __init__(self, detail: str, code: str | None = None, status_code: int = 400):
        super().__init__(detail)
        self.detail = detail
        self.code = code
        self.status_code = status_code


class NotFoundError(AppError):
    """Resource not found error."""
    def __init__(self, detail: str = "Resource not found", code: str = "not_found"):
        super().__init__(detail=detail, code=code, status_code=404)


class UnauthorizedError(AppError):
    """Unauthorized or forbidden access."""
    def __init__(self, detail: str = "Unauthorized", code: str = "unauthorized"):
        super().__init__(detail=detail, code=code, status_code=401)


class RateLimitError(AppError):
    """Rate limit exceeded."""
    def __init__(self, detail: str = "Rate limit exceeded", code: str = "rate_limited"):
        super().__init__(detail=detail, code=code, status_code=429)


def register_exception_handlers(app: FastAPI) -> None:
    """
    Registers exception handlers with the FastAPI application.
    """

    @app.exception_handler(AppError)
    async def app_error_handler(_: Request, exc: AppError):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(detail=exc.detail, code=exc.code).model_dump(),
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception):
        """
        Last-resort handler for unhandled exceptions.
        - Returns generic message by default to avoid leaking details.
        - Adds an X-Request-ID header for correlation.
        - If ENV=development, include a brief debug field.
        Note: /openapi.json and /docs should not be blocked by handler failures;
        upstream fixes ensure OpenAPI generation safely falls back.
        """
        request_id = str(uuid.uuid4())
        settings = get_settings()
        payload = ErrorResponse(detail="Internal Server Error", code="server_error").model_dump()
        if (settings.ENV or "").lower() in ("dev", "development"):
            payload["debug"] = {"path": request.url.path, "method": request.method}
        response = JSONResponse(status_code=500, content=payload)
        response.headers["X-Request-ID"] = request_id
        return response
