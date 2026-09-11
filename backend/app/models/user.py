"""
User and Entrepreneur Profile Models (Section 5, 21.5, 29).
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .common import RiskLevel


class LocationPoint(BaseModel):
    """Geographic Coordinates and Service Radius"""
    latitude: float = Field(..., description="Latitude in decimal degrees", ge=-90.0, le=90.0)
    longitude: float = Field(..., description="Longitude in decimal degrees", ge=-180.0, le=180.0)
    village_or_town: Optional[str] = Field(default="Rural District", description="Village, Town or Block name")
    district: Optional[str] = Field(default="Sample District", description="District name")
    state: Optional[str] = Field(default="Sample State", description="State name")
    service_radius_km: float = Field(default=10.0, description="Service area radius in km (5-15km)", ge=1.0, le=50.0)


class ResourceItem(BaseModel):
    """Owned physical or tangible asset/resource"""
    name: str = Field(..., description="Resource name (e.g. Workspace, 1 Acre Land, 2 Sewing Machines)")
    category: str = Field(default="Equipment", description="Resource type (Land, Equipment, Transport, Raw Materials)")
    condition: str = Field(default="Operational", description="Condition or status")


class EntrepreneurProfile(BaseModel):
    """
    Entrepreneur Capability Profile (Section 5, 21.5, 30).
    Captures skills, available budget, resources, location, interests, and constraints.
    """
    user_id: str = Field(default="user_demo_01", description="Unique identifier for entrepreneur")
    name: str = Field(default="Rural Entrepreneur", description="Entrepreneur full name")
    phone: Optional[str] = Field(default=None, description="Contact phone (private)")
    preferred_language: str = Field(default="English", description="Preferred language for explanations")
    
    # Financial Inputs
    available_capital: float = Field(..., description="Available self-investment capital / budget in INR (₹)", ge=0.0)
    
    # Skills & Experience
    skills: List[str] = Field(default_factory=list, description="Array of demonstrated skills (e.g. ['Handicraft', 'Sewing'])")
    experience_years: float = Field(default=2.0, description="Years of practical or domain experience", ge=0.0)
    
    # Resources & Assets
    resources: List[str] = Field(default_factory=list, description="Owned assets (e.g. ['Workspace', 'Tools', 'Land'])")
    
    # Preferences & Location
    interests: List[str] = Field(default_factory=list, description="Business categories of interest (e.g. ['Handicraft', 'Dairy'])")
    location: LocationPoint = Field(..., description="Location of entrepreneur and enterprise")
    risk_preference: RiskLevel = Field(default=RiskLevel.MEDIUM, description="Risk tolerance (Low, Medium, High)")
    
    # Operational Capabilities (0.0 to 1.0 or qualitative flags)
    has_transport_access: bool = Field(default=False, description="Whether user owns/has direct transport access")
    has_market_connections: bool = Field(default=False, description="Whether user has direct established buyers")
    has_digital_tools: bool = Field(default=False, description="Whether user uses digital payments/smartphones for commerce")
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
