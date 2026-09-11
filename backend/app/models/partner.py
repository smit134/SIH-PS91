"""Partner Discovery and Complementary Matching Models."""

import enum
import uuid
from typing import TYPE_CHECKING, Any, List
from sqlalchemy import BigInteger, Boolean, Enum, ForeignKey, Integer, JSON, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class PartnerVerificationStatus(str, enum.Enum):
    BASIC = "BASIC"
    VERIFIED = "VERIFIED"


class MatchStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class PartnerProfile(Base):
    """Listing information for entrepreneurs seeking complementary business partners."""

    __tablename__ = "partner_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    investment_capacity_min: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
        nullable=False,
        comment="Minimum capital the partner can contribute in INR",
    )
    investment_capacity_max: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
        nullable=False,
        comment="Maximum capital the partner can contribute in INR",
    )
    verification_status: Mapped[PartnerVerificationStatus] = mapped_column(
        Enum(PartnerVerificationStatus, name="partner_verification_enum", native_enum=False),
        default=PartnerVerificationStatus.BASIC,
        nullable=False,
        comment="Profile verification confidence level",
    )
    is_looking_for_partner: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Whether visible in partner recommendation queries",
    )

    user: Mapped["User"] = relationship("User", back_populates="partner_profile")


class PartnerMatch(Base):
    """Calculated synergy matches and mutual-interest consent records."""

    __tablename__ = "partner_matches"

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    partner_user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    synergy_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Synergy score from 0 to 100",
    )
    reasons: Mapped[List[Any]] = mapped_column(
        JSON,
        default=list,
        nullable=False,
        comment="Deterministic matching reasons and complementarity signals",
    )
    status: Mapped[MatchStatus] = mapped_column(
        Enum(MatchStatus, name="match_status_enum", native_enum=False),
        default=MatchStatus.PENDING,
        nullable=False,
        comment="Mutual consent state: PENDING, ACCEPTED, REJECTED",
    )
    initiated_by: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="User ID who initiated the interest",
    )
