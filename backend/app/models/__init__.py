from .common import EvidenceClass, RiskLevel, VerificationState, CapabilityDimension
from .user import EntrepreneurProfile, LocationPoint, ResourceItem
from .business import BusinessCategory, BusinessFitResult, BusinessComparisonResult, FactorBreakdown
from .partner import PartnerProfile, CapabilityGapAnalysis, PartnerSynergyResult, PartnerCard
from .evidence import LocalEvidenceItem, LocalOpportunitySnapshot, POIItem, RegisteredMSMEItem

__all__ = [
    "EvidenceClass",
    "RiskLevel",
    "VerificationState",
    "CapabilityDimension",
    "EntrepreneurProfile",
    "LocationPoint",
    "ResourceItem",
    "BusinessCategory",
    "BusinessFitResult",
    "BusinessComparisonResult",
    "FactorBreakdown",
    "PartnerProfile",
    "CapabilityGapAnalysis",
    "PartnerSynergyResult",
    "PartnerCard",
    "LocalEvidenceItem",
    "LocalOpportunitySnapshot",
    "POIItem",
    "RegisteredMSMEItem",
"""ThinkForge ORM Models Registry.

Exports all database models for Alembic migrations and application usage.
"""

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
from app.models.business import BusinessCategory
from app.models.partner import (
    PartnerProfile,
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

__all__ = [
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
    "BusinessCategory",
    "PartnerProfile",
    "PartnerMatch",
    "PartnerVerificationStatus",
    "MatchStatus",
    "GovernmentScheme",
    "EvidenceRecord",
    "EvidenceReliabilityClass",
    "EvidenceType",
    "AuditLog",
]
