"""
FastAPI Router for Opportunity Intelligence Engine (Part 4 - Aishwarya).
Endpoints for business recommendations, 7-factor scoring, reverse search, and comparison.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from ..core.database import get_db
from ..models.user import EntrepreneurProfile
from ..models.business import (
    BusinessCategory,
    BusinessFitResult,
    BusinessComparisonResult,
    ReverseSearchResult,
)
from ..engines.opportunity_engine import OpportunityEngine
from ..data.business_catalog import get_all_businesses, get_business_by_id


router = APIRouter(prefix="/api/intelligence/opportunity", tags=["Opportunity Intelligence Engine"])


class BusinessComparisonRequest(BaseModel):
    profile: EntrepreneurProfile
    business_ids: List[str]


class SingleBusinessScoreRequest(BaseModel):
    profile: EntrepreneurProfile
    business_id: str


@router.get("/catalog", response_model=List[BusinessCategory], summary="Get all registered business categories in catalog")
async def get_catalog():
    """Returns all supported rural business categories with requirement metadata."""
    return get_all_businesses()


@router.post("/recommendations", response_model=List[BusinessFitResult], summary="Get ranked business recommendations")
async def get_opportunity_recommendations(profile: EntrepreneurProfile, db: AsyncSession = Depends(get_db)):
    """
    Evaluates all business categories against the entrepreneur profile and returns
    deterministic 7-factor fit scores with full explainability.
    """
    search_res = await OpportunityEngine.reverse_business_search(db, profile)
    return search_res.ranked_opportunities


@router.post("/reverse-search", response_model=ReverseSearchResult, summary="USP #2: Reverse Business Search ('Resource -> Business')")
async def reverse_business_search(profile: EntrepreneurProfile, db: AsyncSession = Depends(get_db)):
    """
    'What can I start with what I have?'
    Takes skills, capital, and resources and ranks viable businesses.
    """
    return await OpportunityEngine.reverse_business_search(db, profile)


@router.post("/score-single", response_model=BusinessFitResult, summary="Score a single specific business category")
async def score_single_business(request: SingleBusinessScoreRequest, db: AsyncSession = Depends(get_db)):
    """Calculates detailed fit score and explainability breakdown for a specific category."""
    business = get_business_by_id(request.business_id)
    if not business:
        raise HTTPException(status_code=404, detail=f"Business category '{request.business_id}' not found in catalog.")
    return await OpportunityEngine.score_business(db, request.profile, business)


@router.post("/compare", response_model=BusinessComparisonResult, summary="Compare multiple business opportunities side-by-side")
async def compare_businesses(request: BusinessComparisonRequest, db: AsyncSession = Depends(get_db)):
    """
    Provides side-by-side comparison matrix of fit score, capital, risk, break-even, etc.
    """
    return await OpportunityEngine.compare_businesses(db, request.profile, request.business_ids)


class InteractionRequest(BaseModel):
    user_id: str
    business_id: str
    interaction_type: str  # LIKE, DISLIKE, VIEW

@router.post("/interact", summary="Record a user interaction (Like/Dislike) for an opportunity")
async def record_interaction(request: InteractionRequest, db: AsyncSession = Depends(get_db)):
    """Records the user's choice to power the AI-first personalized recommendations."""
    from ..models.interaction import UserInteraction, InteractionType
    
    # Simple validation
    if request.interaction_type not in ["LIKE", "DISLIKE", "VIEW"]:
        raise HTTPException(400, "Invalid interaction_type. Must be LIKE, DISLIKE, or VIEW.")
        
    uid = request.user_id
        
    interaction = UserInteraction(
        user_id=uid,
        business_id=request.business_id,
        interaction_type=InteractionType(request.interaction_type)
    )
    db.add(interaction)
    await db.commit()
    return {"status": "success", "message": "Interaction recorded"}
