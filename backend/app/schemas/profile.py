"""Profile, Skills, and Physical Asset DTO Schemas."""

from datetime import datetime
from typing import List, Optional
import uuid
from pydantic import BaseModel, ConfigDict, Field

from app.models.profile import ResourceType, RiskTolerance, SkillProficiency


class UserSkillResponse(BaseModel):
    """Skill representation associated with an entrepreneur profile."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    skill_id: uuid.UUID
    name: str
    category: str
    proficiency: SkillProficiency


class SkillCreate(BaseModel):
    """Payload to attach a skill to the user's profile."""

    name: str = Field(..., min_length=2, max_length=100, description="Skill title")
    category: str = Field(
        "PRODUCTION",
        max_length=50,
        description="Domain category (e.g. PRODUCTION, MARKETING, LOGISTICS, CRAFT)",
    )
    proficiency: SkillProficiency = Field(
        SkillProficiency.INTERMEDIATE,
        description="Proficiency level: BEGINNER, INTERMEDIATE, or EXPERT",
    )


class UserResourceResponse(BaseModel):
    """Physical asset representation associated with an entrepreneur profile."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    resource_id: uuid.UUID
    name: str
    resource_type: ResourceType
    details: Optional[str] = None


class ResourceCreate(BaseModel):
    """Payload to attach a physical asset to the user's profile."""

    name: str = Field(..., min_length=2, max_length=100, description="Asset title")
    resource_type: ResourceType = Field(
        ...,
        description="Asset type: LAND, EQUIPMENT, VEHICLE, STORAGE, RAW_MATERIAL, SHOP",
    )
    details: Optional[str] = Field(
        None,
        max_length=255,
        description="Specific metrics (e.g., 2 acres, 5-ton truck, retail counter)",
    )


class ProfileUpdate(BaseModel):
    """Payload to update an entrepreneur capability profile."""

    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    language: Optional[str] = Field(None, min_length=2, max_length=10)
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0)
    approx_location_name: Optional[str] = Field(None, max_length=255)
    service_radius_km: Optional[int] = Field(None, ge=1, le=100)
    available_capital: Optional[int] = Field(None, ge=0)
    risk_tolerance: Optional[RiskTolerance] = None
    experience_years: Optional[int] = Field(None, ge=0, le=70)


class ProfileResponse(BaseModel):
    """Complete entrepreneur profile with skills and physical resources."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    full_name: str
    language: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    approx_location_name: Optional[str] = None
    service_radius_km: int
    available_capital: int
    risk_tolerance: RiskTolerance
    experience_years: int
    skills: List[UserSkillResponse] = []
    resources: List[UserResourceResponse] = []
    created_at: datetime
    updated_at: datetime


class ProfileReadinessResponse(BaseModel):
    """Profile completeness score and capability gap highlights."""

    readiness_percentage: int = Field(..., ge=0, le=100)
    completed_sections: List[str]
    missing_sections: List[str]
    recommendations: List[str]
