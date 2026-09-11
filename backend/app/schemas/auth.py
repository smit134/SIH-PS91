"""Authentication Request and Response DTO Schemas."""

from datetime import datetime
from typing import Any, Dict, Optional
import uuid
from pydantic import BaseModel, ConfigDict, Field

from app.models.user import UserRole


class RegisterRequest(BaseModel):
    """Registration payload for new users."""

    phone: str = Field(
        ...,
        min_length=10,
        max_length=16,
        pattern=r"^\+?[0-9]{10,15}$",
        description="Mobile phone number in E.164 or 10-digit format",
        examples=["+919876543210"],
    )
    password: str = Field(
        ...,
        min_length=6,
        max_length=128,
        description="User password (minimum 6 characters)",
        examples=["secretPass123"],
    )
    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Full name of the entrepreneur",
        examples=["Ramesh Patel"],
    )
    email: Optional[str] = Field(
        None,
        pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        description="Optional email address for communications",
        examples=["ramesh@example.org"],
    )
    language: str = Field(
        "hi",
        min_length=2,
        max_length=10,
        description="Preferred language code (e.g., 'hi' for Hindi, 'en' for English)",
        examples=["hi"],
    )
    role: UserRole = Field(
        default=UserRole.ENTREPRENEUR,
        description="User role on the platform",
    )


class LoginRequest(BaseModel):
    """Login payload."""

    phone: str = Field(
        ...,
        description="Registered phone number",
        examples=["+919876543210"],
    )
    password: str = Field(
        ...,
        description="User account password",
        examples=["secretPass123"],
    )


class RefreshTokenRequest(BaseModel):
    """Token refresh request."""

    refresh_token: str = Field(
        ...,
        description="Valid JWT refresh token",
    )


class UserResponse(BaseModel):
    """Public user response representation (excludes passwords)."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    phone: str
    email: Optional[str] = None
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime


class TokenResponse(BaseModel):
    """Authentication success payload with tokens and user summary."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(
        ...,
        description="Access token lifespan in seconds",
    )
    user: UserResponse


class AuthMeResponse(BaseModel):
    """Current authenticated user information."""

    user: UserResponse
    profile_summary: Optional[Dict[str, Any]] = None


class SendOtpRequest(BaseModel):
    """Mobile number for OTP dispatch."""

    phone: str = Field(
        ...,
        min_length=10,
        max_length=16,
        pattern=r"^\+?[0-9]{10,15}$",
        description="Mobile phone number in E.164 or 10-digit format",
        examples=["+919876543210"],
    )


class SendOtpResponse(BaseModel):
    """OTP dispatch response."""

    message: str
    phone: str
    expires_in_seconds: int
    is_registered_user: bool


class VerifyOtpRequest(BaseModel):
    """Verification payload for phone OTP authentication."""

    phone: str = Field(
        ...,
        min_length=10,
        max_length=16,
        pattern=r"^\+?[0-9]{10,15}$",
        description="Mobile phone number in E.164 or 10-digit format",
    )
    otp_code: str = Field(
        ...,
        min_length=4,
        max_length=8,
        description="Verification code received via SMS",
        examples=["123456"],
    )
    full_name: Optional[str] = Field(
        None,
        description="Full name for automatic onboarding if new user",
        examples=["Gita Devi"],
    )
    language: str = Field(
        "hi",
        description="Language preference if new user",
    )

