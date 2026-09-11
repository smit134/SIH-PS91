"""User and Authentication ORM Models."""

import enum
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.profile import Profile
    from app.models.partner import PartnerProfile
    from app.models.audit import AuditLog


class UserRole(str, enum.Enum):
    ENTREPRENEUR = "ENTREPRENEUR"
    ADVISOR = "ADVISOR"
    ADMIN = "ADMIN"


class User(Base):
    """Core user entity representing registered platform users."""

    __tablename__ = "users"

    phone: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
        nullable=False,
        comment="Primary user contact identifier (E.164 format)",
    )
    email: Mapped[Optional[str]] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=True,
        comment="Optional email address",
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Securely hashed password string",
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role_enum", native_enum=False),
        default=UserRole.ENTREPRENEUR,
        nullable=False,
        comment="User role defining access permissions",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Whether user account is active",
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Phone/Identity verification status",
    )

    # Relationships
    profile: Mapped[Optional["Profile"]] = relationship(
        "Profile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    partner_profile: Mapped[Optional["PartnerProfile"]] = relationship(
        "PartnerProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    audit_logs: Mapped[List["AuditLog"]] = relationship(
        "AuditLog",
        back_populates="user",
        cascade="all, delete-orphan",
    )
