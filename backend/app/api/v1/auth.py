"""Authentication Router: Registration, Login, Token Refresh, and Current User."""

import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import secrets
from app.config import settings
from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.core.exceptions import ConflictException, UnauthorizedException
from app.core.otp import otp_manager
from app.core.rate_limiter import auth_rate_limiter, otp_send_rate_limiter
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.audit import AuditLog
from app.models.profile import Profile
from app.models.user import User
from app.schemas.auth import (
    AuthMeResponse,
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    SendOtpRequest,
    SendOtpResponse,
    TokenResponse,
    UserResponse,
    VerifyOtpRequest,
)

router = APIRouter()



@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new rural entrepreneur",
    description="Registers a new user, hashes password, initializes capability profile, and returns authentication tokens.",
)
async def register_user(
    payload: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    # Verify phone number uniqueness
    existing_phone = await db.execute(
        select(User).where(User.phone == payload.phone)
    )
    if existing_phone.scalar_one_or_none():
        raise ConflictException(
            message="A user with this mobile number is already registered."
        )

    # Verify email uniqueness if provided
    if payload.email:
        existing_email = await db.execute(
            select(User).where(User.email == payload.email)
        )
        if existing_email.scalar_one_or_none():
            raise ConflictException(
                message="A user with this email address is already registered."
            )

    # Hash password securely
    hashed_pwd = hash_password(payload.password)

    # Create User record
    user = User(
        phone=payload.phone,
        email=payload.email,
        hashed_password=hashed_pwd,
        role=payload.role,
        is_active=True,
        is_verified=False,
    )
    db.add(user)
    await db.flush()

    # Initialize capability profile
    profile = Profile(
        user_id=user.id,
        full_name=payload.full_name,
        language=payload.language,
        available_capital=0,
    )
    db.add(profile)

    # Record registration audit event
    audit = AuditLog(
        user_id=user.id,
        action="USER_REGISTERED",
        resource_type="USER",
        resource_id=str(user.id),
        details={"phone": user.phone, "role": user.role.value},
    )
    db.add(audit)
    await db.commit()
    await db.refresh(user)

    # Issue JWT tokens
    access_token = create_access_token(
        subject=str(user.id),
        claims={"phone": user.phone, "role": user.role.value},
    )
    refresh_token = create_refresh_token(subject=str(user.id))

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(user),
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate user and issue JWT tokens",
)
async def login_user(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    query = select(User).where(User.phone == payload.phone)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise UnauthorizedException(
            message="Invalid mobile number or password."
        )

    if not user.is_active:
        raise UnauthorizedException(
            message="Your user account has been disabled. Please contact support."
        )

    # Log successful login event
    audit = AuditLog(
        user_id=user.id,
        action="AUTH_LOGIN_SUCCESS",
        resource_type="USER",
        resource_id=str(user.id),
        details={"phone": user.phone},
    )
    db.add(audit)
    await db.commit()

    # Generate tokens
    access_token = create_access_token(
        subject=str(user.id),
        claims={"phone": user.phone, "role": user.role.value},
    )
    refresh_token = create_refresh_token(subject=str(user.id))

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(user),
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh access token using valid refresh token",
)
async def refresh_tokens(
    payload: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    token_payload = decode_token(payload.refresh_token, expected_type="refresh")
    user_id_str = token_payload.get("sub")
    if not user_id_str:
        raise UnauthorizedException(message="Malformed refresh token.")

    try:
        user_uuid = uuid.UUID(user_id_str)
    except ValueError:
        raise UnauthorizedException(message="Invalid user identifier.")

    user = await db.get(User, user_uuid)
    if not user or not user.is_active:
        raise UnauthorizedException(message="User account is invalid or deactivated.")

    # Issue fresh token pair
    new_access_token = create_access_token(
        subject=str(user.id),
        claims={"phone": user.phone, "role": user.role.value},
    )
    new_refresh_token = create_refresh_token(subject=str(user.id))

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(user),
    )


@router.get(
    "/me",
    response_model=AuthMeResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current authenticated user profile",
)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user),
):
    profile_summary = None
    if current_user.profile:
        profile_summary = {
            "full_name": current_user.profile.full_name,
            "language": current_user.profile.language,
            "available_capital": current_user.profile.available_capital,
            "risk_tolerance": current_user.profile.risk_tolerance.value,
            "approx_location": current_user.profile.approx_location_name,
        }

    return AuthMeResponse(
        user=UserResponse.model_validate(current_user),
        profile_summary=profile_summary,
    )


@router.post(
    "/otp/send",
    response_model=SendOtpResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(otp_send_rate_limiter)],
    summary="Request a verification OTP via SMS",
    description="Dispatches a 6-digit numeric OTP to the entrepreneur's mobile number with 5-minute expiry.",
)
async def send_otp(
    payload: SendOtpRequest,
    db: AsyncSession = Depends(get_db),
):
    existing_user = await db.execute(
        select(User).where(User.phone == payload.phone)
    )
    is_registered = existing_user.scalar_one_or_none() is not None

    _, ttl = otp_manager.generate_otp(payload.phone)

    return SendOtpResponse(
        message=f"OTP successfully dispatched to {payload.phone}.",
        phone=payload.phone,
        expires_in_seconds=ttl,
        is_registered_user=is_registered,
    )


@router.post(
    "/otp/verify",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(auth_rate_limiter)],
    summary="Verify mobile OTP and authenticate/onboard",
    description="Verifies the 6-digit code. If user exists, signs them in. If new user, automatically creates an account and capability profile.",
)
async def verify_otp(
    payload: VerifyOtpRequest,
    db: AsyncSession = Depends(get_db),
):
    otp_manager.verify_otp(payload.phone, payload.otp_code)

    res = await db.execute(select(User).where(User.phone == payload.phone))
    user = res.scalar_one_or_none()

    if not user:
        # Auto-register new entrepreneur via phone verification
        random_password = secrets.token_urlsafe(24)
        user = User(
            phone=payload.phone,
            hashed_password=hash_password(random_password),
            is_active=True,
            is_verified=True,
        )
        db.add(user)
        await db.flush()

        profile = Profile(
            user_id=user.id,
            full_name=payload.full_name or "Rural Entrepreneur",
            language=payload.language,
        )
        db.add(profile)

        audit = AuditLog(
            user_id=user.id,
            action="USER_REGISTER_OTP",
            resource_type="USER",
            resource_id=str(user.id),
            details={"phone": user.phone, "onboarding": "sms_otp"},
        )
        db.add(audit)
        await db.commit()
        await db.refresh(user)
    else:
        if not user.is_active:
            raise UnauthorizedException(message="Account has been deactivated.")

        audit = AuditLog(
            user_id=user.id,
            action="USER_LOGIN_OTP",
            resource_type="USER",
            resource_id=str(user.id),
            details={"phone": user.phone, "method": "sms_otp"},
        )
        db.add(audit)
        await db.commit()

    access_token = create_access_token(
        subject=str(user.id),
        claims={"phone": user.phone, "role": user.role.value},
    )
    refresh_token = create_refresh_token(subject=str(user.id))

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(user),
    )

