"""
Configuration & Deterministic Weights for ThinkForge Intelligence Engines.
Section 6, 24, and 25 of Project Specification.
"""

from pydantic import BaseModel, Field


class OpportunityScoringWeights(BaseModel):
    """Configurable weights for Opportunity Fit Scoring (Section 24)"""
    capital_fit: float = Field(default=0.20, description="Capital Fit Weight (20%)")
    skill_fit: float = Field(default=0.20, description="Skill Fit Weight (20%)")
    resource_fit: float = Field(default=0.15, description="Resource Fit Weight (15%)")
    local_opportunity: float = Field(default=0.20, description="Local Opportunity Signal Weight (20%)")
    market_access: float = Field(default=0.10, description="Market Accessibility Weight (10%)")
    margin_potential: float = Field(default=0.10, description="Margin Potential Weight (10%)")
    risk_suitability: float = Field(default=0.05, description="Risk Suitability Weight (5%)")


class PartnerSynergyWeights(BaseModel):
    """Configurable weights for Partner Synergy Scoring (Section 6 & 25)"""
    skill_complementarity: float = Field(default=0.30, description="Skill Complementarity Weight (30%)")
    capital_compatibility: float = Field(default=0.20, description="Capital Compatibility Weight (20%)")
    resource_complementarity: float = Field(default=0.15, description="Resource Complementarity Weight (15%)")
    shared_interest: float = Field(default=0.15, description="Shared Business Interest Weight (15%)")
    location_proximity: float = Field(default=0.10, description="Geographic Proximity Weight (10%)")
    experience_compatibility: float = Field(default=0.10, description="Experience Compatibility Weight (10%)")


class EngineSettings:
    DEFAULT_SERVICE_RADIUS_KM: float = 10.0
    MAX_PARTNER_RADIUS_KM: float = 50.0
    DEFAULT_OPPORTUNITY_WEIGHTS: OpportunityScoringWeights = OpportunityScoringWeights()
    DEFAULT_SYNERGY_WEIGHTS: PartnerSynergyWeights = PartnerSynergyWeights()


settings = EngineSettings()
