"""ThinkForge Custom Exceptions and Global Handlers.

Enforces uniform RFC-compliant JSON error envelopes across all API endpoints.
"""

import logging
from typing import Any, Optional
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.schemas.common import ErrorDetail, ErrorResponse

logger = logging.getLogger("thinkforge.exceptions")


class APIException(Exception):
    """Base API Exception for ThinkForge."""

    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        code: str = "INTERNAL_ERROR",
        message: str = "An unexpected error occurred.",
        details: Optional[Any] = None,
    ):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details
        super().__init__(self.message)


class NotFoundException(APIException):
    def __init__(self, message: str = "Resource not found.", details: Optional[Any] = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="RESOURCE_NOT_FOUND",
            message=message,
            details=details,
        )


class UnauthorizedException(APIException):
    def __init__(self, message: str = "Authentication required.", details: Optional[Any] = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="UNAUTHORIZED",
            message=message,
            details=details,
        )


class ForbiddenException(APIException):
    def __init__(self, message: str = "Access forbidden.", details: Optional[Any] = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            code="FORBIDDEN_RESOURCE",
            message=message,
            details=details,
        )


class ConflictException(APIException):
    def __init__(self, message: str = "Resource conflict.", details: Optional[Any] = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            code="RESOURCE_CONFLICT",
            message=message,
            details=details,
        )


class ValidationException(APIException):
    def __init__(self, message: str = "Validation failed.", details: Optional[Any] = None):
        super().__init__(
            status_code=getattr(status, "HTTP_422_UNPROCESSABLE_CONTENT", 422),
            code="VALIDATION_ERROR",
            message=message,
            details=details,
        )


async def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    """Handles custom APIException instances."""
    error_payload = ErrorResponse(
        error=ErrorDetail(
            code=exc.code,
            message=exc.message,
            details=exc.details,
        )
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_payload.model_dump(mode="json"),
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handles Pydantic request validation errors."""
    sanitized_errors = []
    for error in exc.errors():
        loc = list(error.get("loc", []))
        # Strip internal 'body' identifier if present for cleaner frontend consumption
        field = " -> ".join(str(l) for l in loc if l != "body") or "payload"
        sanitized_errors.append(
            {
                "field": field,
                "message": error.get("msg", "Invalid input"),
                "type": error.get("type", "value_error"),
            }
        )

    error_payload = ErrorResponse(
        error=ErrorDetail(
            code="VALIDATION_ERROR",
            message="Request input validation failed.",
            details=sanitized_errors,
        )
    )
    return JSONResponse(
        status_code=getattr(status, "HTTP_422_UNPROCESSABLE_CONTENT", 422),
        content=error_payload.model_dump(mode="json"),
    )


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """Handles standard Starlette/FastAPI HTTPException instances."""
    code_map = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN_RESOURCE",
        404: "RESOURCE_NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        409: "RESOURCE_CONFLICT",
        422: "VALIDATION_ERROR",
        500: "INTERNAL_ERROR",
    }
    code = code_map.get(exc.status_code, "API_ERROR")
    message = str(exc.detail) if exc.detail else "An HTTP error occurred."

    error_payload = ErrorResponse(
        error=ErrorDetail(
            code=code,
            message=message,
            details=None,
        )
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_payload.model_dump(mode="json"),
        headers=getattr(exc, "headers", None),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catches all uncaught exceptions to prevent leakage of internal stack traces."""
    logger.exception(f"Unhandled server exception on {request.method} {request.url.path}: {exc}")

    error_payload = ErrorResponse(
        error=ErrorDetail(
            code="INTERNAL_ERROR",
            message="An internal server error occurred. Please contact system support.",
            details=None,
        )
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_payload.model_dump(mode="json"),
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Registers all custom exception handlers to the FastAPI app instance."""
    app.add_exception_handler(APIException, api_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
