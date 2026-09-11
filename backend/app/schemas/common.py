"""Standard Response and Error Schemas.

Consistent across all endpoints in ThinkForge API.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    code: str = Field(..., description="Standardized error code identifier")
    message: str = Field(..., description="Human readable explanation of the error")
    details: Optional[Any] = Field(None, description="Detailed validation errors or context")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp when error occurred",
    )


class ErrorResponse(BaseModel):
    error: ErrorDetail


class HealthResponse(BaseModel):
    status: str = Field("ok", description="Overall service status")
    version: str = Field(..., description="Application version")
    environment: str = Field(..., description="Current running environment")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Server UTC timestamp",
    )
