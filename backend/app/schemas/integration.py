"""Pydantic schemas and interface contracts for team member integrations."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ==========================================
# 1. Aishwarya's Contract (Feasibility & Partners)
# ==========================================

class BusinessRecommendationResponse(BaseModel):
    category_code: str
    category_name: str
    feasibility_score: float = Field(..., ge=0.0, le=100.0)
    risk_level: str
    capital_required: int
    break_even_months: int
    rationale: str
    key_drivers: List[str] = []


class PartnerMatchResponse(BaseModel):
    partner_id: str
    partner_name: str
    approx_location: Optional[str] = None
    distance_km: Optional[float] = None
    synergy_score: float = Field(..., ge=0.0, le=100.0)
    complementary_skills: List[str] = []
    contact_status: str = "AVAILABLE"


# ==========================================
# 2. Kesha's Contract (Finance & Schemes)
# ==========================================

class FinanceSimulationRequest(BaseModel):
    capital_invested: float = Field(..., gt=0)
    monthly_revenue_projected: float = Field(..., ge=0)
    monthly_expenses_projected: float = Field(..., ge=0)


class FinanceSimulationResponse(BaseModel):
    capital_invested: float
    monthly_net_profit: float
    profit_margin_pct: float
    break_even_months: float
    runway_months: float
    is_viable: bool


class SchemeMatchResponse(BaseModel):
    scheme_id: str
    scheme_name: str
    short_code: str
    max_loan_amount: int
    subsidy_percentage: float
    interest_rate_annual: float
    authority_name: str
    eligibility_verdict: str  # e.g., "HIGHLY_ELIGIBLE", "ELIGIBLE", "POTENTIAL"
    matched_criteria: List[str] = []
    official_source_url: Optional[str] = None


# ==========================================
# 3. Smit's Contract (Field Evidence & Ground Truth)
# ==========================================

class EvidenceNearbyResponse(BaseModel):
    evidence_id: str
    source_name: str
    evidence_type: str
    reliability_class: str
    confidence_score: int
    payload: Dict[str, Any] = {}
    distance_km: Optional[float] = None
    fetched_at: datetime

