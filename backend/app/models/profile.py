"""Entrepreneur Capability Profile and Resource Models."""

import enum
import uuid
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import BigInteger, Enum, Float, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class RiskTolerance(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class SkillProficiency(str, enum.Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    EXPERT = "EXPERT"


class ResourceType(str, enum.Enum):
    LAND = "LAND"
    EQUIPMENT = "EQUIPMENT"
    VEHICLE = "VEHICLE"
    STORAGE = "STORAGE"
    RAW_MATERIAL = "RAW_MATERIAL"
    SHOP = "SHOP"


class Profile(Base):
    """Entrepreneur Capability Profile capturing skills, capital, resources, and geography."""

    __tablename__ = "profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Full name of the entrepreneur",
    )
    language: Mapped[str] = mapped_column(
        String(10),
        default="hi",
        nullable=False,
        comment="Preferred communication language (e.g. hi, en)",
    )
    latitude: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="Location latitude in WGS 84",
    )
    longitude: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="Location longitude in WGS 84",
    )
    approx_location_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Village / Taluka / District name",
    )
    service_radius_km: Mapped[int] = mapped_column(
        Integer,
        default=10,
        nullable=False,
        comment="Operational radius in kilometers (typically 5-10 km)",
    )
    available_capital: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
        nullable=False,
        comment="Available budget/capital in INR",
    )
    risk_tolerance: Mapped[RiskTolerance] = mapped_column(
        Enum(RiskTolerance, name="risk_tolerance_enum", native_enum=False),
        default=RiskTolerance.MEDIUM,
        nullable=False,
        comment="Entrepreneur risk appetite",
    )
    experience_years: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Years of commercial or artisanal experience",
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="profile")
    skills: Mapped[List["UserSkill"]] = relationship(
        "UserSkill", back_populates="profile", cascade="all, delete-orphan"
    )
    resources: Mapped[List["UserResource"]] = relationship(
        "UserResource", back_populates="profile", cascade="all, delete-orphan"
    )


class Skill(Base):
    """Taxonomy of rural skills and capabilities."""

    __tablename__ = "skills"

    name: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    category: Mapped[str] = mapped_column(
        String(50), index=True, nullable=False, comment="Production, Marketing, Logistics, etc."
    )


class UserSkill(Base):
    """Mapping table for entrepreneur skills with proficiency ratings."""

    __tablename__ = "user_skills"

    profile_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    skill_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("skills.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    proficiency: Mapped[SkillProficiency] = mapped_column(
        Enum(SkillProficiency, name="skill_proficiency_enum", native_enum=False),
        default=SkillProficiency.INTERMEDIATE,
        nullable=False,
    )

    profile: Mapped["Profile"] = relationship("Profile", back_populates="skills")
    skill: Mapped["Skill"] = relationship("Skill")


class Resource(Base):
    """Physical assets and infrastructural resources."""

    __tablename__ = "resources"

    name: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    resource_type: Mapped[ResourceType] = mapped_column(
        Enum(ResourceType, name="resource_type_enum", native_enum=False),
        nullable=False,
        index=True,
    )


class UserResource(Base):
    """Mapping of physical assets owned or accessible by the entrepreneur."""

    __tablename__ = "user_resources"

    profile_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    resource_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("resources.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    details: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Specifics like acreage, machine model, or vehicle capacity",
    )

    profile: Mapped["Profile"] = relationship("Profile", back_populates="resources")
    resource: Mapped["Resource"] = relationship("Resource")
