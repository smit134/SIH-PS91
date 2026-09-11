"""
Business Idea, Category and Opportunity Scoring Models (Section 7, 8, 13, 21.5, 24).
"""

from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from .common import RiskLevel, EvidenceClass


class BusinessRequirement(BaseModel):
    """Specific skill, resource and financial requirements for a business category"""
    required_skills: List[str] = Field(..., description="Essential skills needed for this business")
    optional_skills: List[str] = Field(default_factory=list, description="Helpful non-critical skills")
    required_resources: List[str] = Field(..., description="Required assets (e.g. ['Workspace', 'Power', 'Water'])")
    min_capital_required: float = Field(..., description="Minimum startup capital in INR (₹)")
    recommended_capital: float = Field(..., description="Recommended capital in INR (₹)")
    estimated_monthly_operating_cost: float = Field(..., description="Estimated monthly operating cost in INR (₹)")
    estimated_monthly_revenue: float = Field(..., description="Estimated baseline monthly revenue in INR (₹)")
    break_even_months_estimate: int = Field(default=12, description="Estimated break-even duration in months")
    typical_margin_percentage: float = Field(default=25.0, description="Typical gross profit margin %")
    inherent_risk: RiskLevel = Field(default=RiskLevel.MEDIUM, description="Inherent business risk level")


class BusinessCategory(BaseModel):
    """Catalog entry for a rural business opportunity"""
    id: str = Field(..., description="Unique business category identifier (e.g. 'handicraft_textiles')")
    name: str = Field(..., description="Business category display name (e.g. 'Handicraft & Textile Products')")
    sector: str = Field(..., description="Sector (e.g. 'Artisanal & Crafts', 'Agri-Business', 'Food Processing')")
    description: str = Field(..., description="Summary description of the business model")
    requirements: BusinessRequirement = Field(..., description="Detailed requirements")
    tags: List[str] = Field(default_factory=list, description="Keywords and tags")


class FactorBreakdown(BaseModel):
    """Individual 0-100 scores for the 7 opportunity scoring dimensions (Section 8 & 24)"""
    capital_fit: float = Field(..., description="Capital Fit score (0-100)", ge=0.0, le=100.0)
    skill_fit: float = Field(..., description="Skill Fit score (0-100)", ge=0.0, le=100.0)
    resource_fit: float = Field(..., description="Resource Fit score (0-100)", ge=0.0, le=100.0)
    local_opportunity: float = Field(..., description="Local Opportunity Signal score (0-100)", ge=0.0, le=100.0)
    market_access: float = Field(..., description="Market Accessibility score (0-100)", ge=0.0, le=100.0)
    margin_potential: float = Field(..., description="Margin Potential score (0-100)", ge=0.0, le=100.0)
    risk_suitability: float = Field(..., description="Risk Suitability score (0-100)", ge=0.0, le=100.0)


class BusinessFitResult(BaseModel):
    """
    Complete Result of Opportunity Scoring for a Business Category (Section 8 & 24)
    Includes Explainability ("Why recommended", "Why not perfect", "Why NOT this business").
    """
    business_id: str
    business_name: str
    sector: str
    overall_fit_score: float = Field(..., description="Overall Business Fit Score (0-100)", ge=0.0, le=100.0)
    evidence_confidence_score: float = Field(..., description="Evidence Confidence Score (0-100)", ge=0.0, le=100.0)
    evidence_class: EvidenceClass = Field(default=EvidenceClass.DERIVED)
    
    # Factor breakdown
    factor_breakdown: FactorBreakdown
    
    # Financial snapshot
    capital_required_min: float
    capital_required_rec: float
    estimated_monthly_profit: float
    estimated_break_even_months: int
    inherent_risk: RiskLevel
    
    # Explainability layer (Section 8)
    why_recommended: List[str] = Field(default_factory=list, description="Key driving strengths/factors")
    why_not_perfect: List[str] = Field(default_factory=list, description="Limitations or partial matches")
    why_not_this_business: Optional[List[str]] = Field(default=None, description="Clear rejection rationale if low fit")
    confidence_limitations: List[str] = Field(default_factory=list, description="Explanation of missing local evidence")


class BusinessComparisonResult(BaseModel):
    """Side-by-side comparison of multiple business candidates (Section 13)"""
    businesses: List[BusinessFitResult]
    comparison_table: List[Dict[str, str]]
    highest_fit_business_id: str
    lowest_risk_business_id: str
    fastest_breakeven_business_id: str


class ReverseSearchResult(BaseModel):
    """Result of 'What can I start with what I have?' Reverse Search (USP #2 / Section 7)"""
    total_evaluated: int
    ranked_opportunities: List[BusinessFitResult]
    top_recommended: BusinessFitResult
    available_resource_summary: List[str]
    identified_skill_strengths: List[str]
