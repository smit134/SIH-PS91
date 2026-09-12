"""
Partner Matching, Capability Gaps, and Synergy Models (Section 6, 15, 21.5, 25).
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from .common import VerificationState, CapabilityDimension, RiskLevel
from .user import LocationPoint


class CapabilityGapAnalysis(BaseModel):
    """
    Capability Dashboard & Gap Detection (Section 6 & 15).
    Evaluates 6 dimensions: Production, Capital, Marketing, Distribution, Technology, Management.
    """
    dimension_scores: Dict[CapabilityDimension, float] = Field(..., description="0-100% score per capability dimension")
    biggest_gaps: List[str] = Field(..., description="Ranked list of biggest missing capabilities (e.g. ['Marketing', 'Capital'])")
    strongest_capabilities: List[str] = Field(..., description="Ranked list of top strengths")
    summary: str = Field(..., description="High-level narrative of entrepreneur profile capability standing")


class PartnerProfile(BaseModel):
    """
    Partner Profile in Candidate Database (Section 6, 21.5).
    """
    partner_id: str = Field(..., description="Unique partner identifier")
    name: str = Field(..., description="Partner name (masked before consent)")
    phone: Optional[str] = Field(default=None, description="Contact phone (private)")
    location: LocationPoint = Field(..., description="Geographic location")
    
    # Strengths and Assets offered
    capabilities: List[str] = Field(default_factory=list, description="Array of demonstrated strengths (e.g. ['Marketing', 'Capital', 'Transport'])")
    skills: List[str] = Field(default_factory=list, description="Domain skills (e.g. ['Sales', 'Digital Marketing'])")
    resources: List[str] = Field(default_factory=list, description="Available assets/tools (e.g. ['Delivery Van', 'Shop Space'])")
    investment_min: float = Field(default=0.0, description="Minimum capital willing to invest (₹)")
    investment_max: float = Field(default=0.0, description="Maximum capital willing to invest (₹)")
    experience_years: float = Field(default=3.0, description="Years in business or trade")
    
    # Interests & verification
    business_interests: List[str] = Field(default_factory=list, description="Sectors or categories partner is interested in")
    verification_state: VerificationState = Field(default=VerificationState.BASIC, description="Verification status (BASIC, VERIFIED)")


class SynergyFactorBreakdown(BaseModel):
    """Individual 0-100 scores for the 6 synergy scoring dimensions (Section 6 & 25)"""
    skill_complementarity: float = Field(..., description="Skill Complementarity score (0-100)")
    capital_compatibility: float = Field(..., description="Capital Compatibility score (0-100)")
    resource_complementarity: float = Field(..., description="Resource Complementarity score (0-100)")
    shared_interest: float = Field(..., description="Shared Interest score (0-100)")
    location_proximity: float = Field(..., description="Location Proximity score (0-100)")
    experience_compatibility: float = Field(..., description="Experience Compatibility score (0-100)")


class PartnerSynergyResult(BaseModel):
    """Result of Partner Matching & Synergy Calculation (Section 6 & 25)"""
    partner_id: str
    synergy_score: float = Field(..., description="Overall Synergy Score (0-100)", ge=0.0, le=100.0)
    distance_km: float = Field(..., description="Geodesic distance between user and partner in km")
    factor_breakdown: SynergyFactorBreakdown
    match_reasons: List[str] = Field(..., description="List of positive matching factors (e.g. ['✓ Skill complementarity'])")
    unmet_gaps: List[str] = Field(default_factory=list, description="Gaps that this partner cannot resolve")


class PartnerCard(BaseModel):
    """
    Privacy-Preserving Partner Card for UI presentation (Section 6, 15, 33).
    Protects private phone/exact address until mutual consent.
    """
    partner_id: str
    display_title: str = Field(..., description="e.g. 'Partner (Marketing & Capital Specialist)'")
    approximate_area: str = Field(..., description="e.g. 'Within 8 km (District Central Market)'")
    distance_km: float
    key_strengths: List[str]
    investment_range_str: str = Field(..., description="e.g. '₹1,00,000 – ₹3,00,000'")
    shared_interests: List[str]
    synergy_score: float
    verification_state: VerificationState
    why_matched: List[str]
    is_contact_shared: bool = Field(default=False, description="Whether mutual consent is completed")
    contact_phone: Optional[str] = Field(default=None, description="Only provided when mutual consent is true")
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


class PartnerProfileModel(Base):
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
