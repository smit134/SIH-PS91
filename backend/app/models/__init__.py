"""ThinkForge Models Registry.

Exports all database models for Alembic migrations and Pydantic schemas for API usage.
"""

from .common import EvidenceClass, RiskLevel, VerificationState, CapabilityDimension
from .user import EntrepreneurProfile, LocationPoint, ResourceItem
from .business import BusinessCategory, BusinessFitResult, BusinessComparisonResult, FactorBreakdown, BusinessCategoryModel
from .partner import PartnerProfile, PartnerProfileModel, CapabilityGapAnalysis, PartnerSynergyResult, PartnerCard
from .evidence import LocalEvidenceItem, LocalOpportunitySnapshot, POIItem, RegisteredMSMEItem

from app.core.database import Base
from app.models.user import User, UserRole
from app.models.profile import (
    Profile,
    Skill,
    UserSkill,
    Resource,
    UserResource,
    RiskTolerance,
    SkillProficiency,
    ResourceType,
)
from app.models.partner import (
    PartnerMatch,
    PartnerVerificationStatus,
    MatchStatus,
)
from app.models.scheme import GovernmentScheme
from app.models.evidence import (
    EvidenceRecord,
    EvidenceReliabilityClass,
    EvidenceType,
)
from app.models.audit import AuditLog
from app.models.osm_poi import OSMPointOfInterest
from app.models.district_stats import DistrictMSMEStats
from app.models.document_chunk import SchemeDocumentChunk

__all__ = [
    # Pydantic Schemas
    "EvidenceClass",
    "RiskLevel",
    "VerificationState",
    "CapabilityDimension",
    "EntrepreneurProfile",
    "LocationPoint",
    "ResourceItem",
    "BusinessFitResult",
    "BusinessComparisonResult",
    "FactorBreakdown",
    "CapabilityGapAnalysis",
    "PartnerSynergyResult",
    "PartnerCard",
    "LocalEvidenceItem",
    "LocalOpportunitySnapshot",
    "POIItem",
    "RegisteredMSMEItem",

    # ORM Models
    "Base",
    "User",
    "UserRole",
    "Profile",
    "Skill",
    "UserSkill",
    "Resource",
    "UserResource",
    "RiskTolerance",
    "SkillProficiency",
    "ResourceType",
    "BusinessCategoryModel",
    "PartnerProfile",
    "PartnerProfileModel",
    "PartnerMatch",
    "PartnerVerificationStatus",
    "MatchStatus",
    "GovernmentScheme",
    "EvidenceRecord",
    "EvidenceReliabilityClass",
    "EvidenceType",
    "AuditLog",
    "OSMPointOfInterest",
    "DistrictMSMEStats",
    "SchemeDocumentChunk",
]

