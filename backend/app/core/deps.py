"""FastAPI Dependencies for Authentication, Database Sessions, and RBAC."""

from typing import AsyncGenerator, Callable, Optional
import uuid
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from app.config import settings
from app.core.database import get_db
from app.core.exceptions import ForbiddenException, UnauthorizedException
from app.core.security import decode_token
from app.models.user import User, UserRole

# OAuth2 scheme for Swagger UI integration
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    auto_error=False,
)


async def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Authenticates the Bearer JWT token and loads the active user from the database.

    Raises UnauthorizedException on missing, invalid, or expired tokens.
    """
    if not token:
        raise UnauthorizedException(
            message="Authentication credentials were not provided."
        )

    payload = decode_token(token, expected_type="access")
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise UnauthorizedException(message="Malformed token claims.")

    try:
        user_uuid = uuid.UUID(user_id_str)
    except ValueError:
        raise UnauthorizedException(message="Invalid user identifier in token.")

    query = (
        select(User)
        .where(User.id == user_uuid)
        .options(selectinload(User.profile))
    )
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise UnauthorizedException(message="User associated with this token no longer exists.")

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Ensures the authenticated user account is active."""
    if not current_user.is_active:
        raise ForbiddenException(message="User account has been deactivated.")
    return current_user


def require_role(required_role: UserRole) -> Callable:
    """Dependency factory enforcing Role-Based Access Control (RBAC).

    Admins always have supervisory access across all protected role endpoints.
    """

    async def role_checker(
        current_user: User = Depends(get_current_active_user),
    ) -> User:
        if current_user.role != required_role and current_user.role != UserRole.ADMIN:
            raise ForbiddenException(
                message=f"Access requires '{required_role.value}' privileges."
            )
        return current_user

    return role_checker
