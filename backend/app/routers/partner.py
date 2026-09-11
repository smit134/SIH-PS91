"""
FastAPI Router for Partner Engine & Capability Gap Logic (Part 4 - Aishwarya).
Endpoints for capability gap detection, complementary partner matching, and privacy consent.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ..models.user import EntrepreneurProfile
from ..models.partner import (
    PartnerCard,
    CapabilityGapAnalysis,
    PartnerSynergyResult,
)
from ..engines.capability_gap_engine import CapabilityGapEngine
from ..engines.partner_engine import PartnerEngine
from ..data.sample_partners import SAMPLE_PARTNERS


router = APIRouter(prefix="/api/intelligence/partner", tags=["Partner & Capability Gap Engine"])


class ContactRevealRequest(BaseModel):
    partner_id: str
    user_id: str


@router.post("/gap-analysis", response_model=CapabilityGapAnalysis, summary="Evaluate 6D capability dashboard and biggest gaps")
async def evaluate_capability_gaps(profile: EntrepreneurProfile):
    """
    Evaluates Production, Capital, Marketing, Distribution, Technology, Management.
    Identifies biggest capability gaps and strongest pillars.
    """
    return CapabilityGapEngine.evaluate_capabilities(profile)


@router.post("/recommendations", response_model=List[PartnerCard], summary="USP #1: Find Complementary Partners")
async def find_partners(
    profile: EntrepreneurProfile,
    max_radius_km: float = Query(default=50.0, description="Max search radius in km"),
    min_synergy_score: float = Query(default=50.0, description="Minimum synergy threshold (0-100)")
):
    """
    Finds nearby partners whose strengths fill the entrepreneur's capability gaps.
    Returns privacy-preserving partner cards with synergy breakdown.
    """
    return PartnerEngine.find_complementary_partners(
        profile=profile,
        max_radius_km=max_radius_km,
        min_synergy_score=min_synergy_score
    )


@router.post("/request-contact", summary="Mutual-interest consent flow to reveal verified contact details")
async def request_partner_contact(request: ContactRevealRequest):
    """
    Reveals partner contact details only when mutual interest / consent is confirmed.
    """
    contact_data = PartnerEngine.reveal_partner_contact(request.partner_id)
    if not contact_data:
        raise HTTPException(status_code=404, detail=f"Partner '{request.partner_id}' not found.")
    return contact_data
