"""
Common Enumerations and Shared Data Structures for ThinkForge Intelligence Module.
"""

from enum import Enum


class EvidenceClass(str, Enum):
    """Evidence Classification (Section 1, 18, 45)"""
    VERIFIED = "VERIFIED"     # Directly supported by a source
    DERIVED = "DERIVED"       # Calculated from verified inputs
    ESTIMATED = "ESTIMATED"   # Model / heuristic estimate
    UNKNOWN = "UNKNOWN"       # Insufficient evidence


class RiskLevel(str, Enum):
    """Business and Venture Risk Levels"""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class VerificationState(str, Enum):
    """Partner Profile Verification State (Section 6, 15, 21.5)"""
    BASIC = "BASIC"
    VERIFIED = "VERIFIED"


class CapabilityDimension(str, Enum):
    """6 Core Capability Dimensions (Section 6 & 15)"""
    PRODUCTION = "Production"
    CAPITAL = "Capital"
    MARKETING = "Marketing"
    DISTRIBUTION = "Distribution"
    TECHNOLOGY = "Technology"
    MANAGEMENT = "Management"
