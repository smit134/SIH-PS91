from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from app.models.financials import UserProfile, SchemeMatchItem
from app.services.scheme_engine import match_schemes, get_all_schemes
from app.data.business_catalog import get_business_by_id

router = APIRouter(
    prefix="/schemes",
    tags=["schemes"]
)

class SchemeMatchRequest(BaseModel):
    user_profile: Optional[UserProfile] = None
    project_cost: float = 150000.0
    business_category: str = "all"


@router.get("", response_model=List[SchemeMatchItem])
@router.get("/", response_model=List[SchemeMatchItem])
def list_schemes(
    opportunity_id: Optional[str] = Query(None, description="Optional business opportunity ID (e.g., dairy_micro_farm, food_processing_spices)"),
    project_cost: Optional[float] = Query(None, description="Project capex/cost for subsidy calculations"),
    user_capital: Optional[float] = Query(None, description="User available equity"),
    primary_skill: Optional[str] = Query(None, description="User primary vocational skill"),
    sector_interest: Optional[str] = Query(None, description="User sector interest"),
    district: Optional[str] = Query(None, description="User district location"),
    state: Optional[str] = Query(None, description="User state location")
):
    """
    Returns government schemes, matched and personalized according to:
    - Target business opportunity
    - Project capital cost
    - User's specific capability inputs (equity, skills, location, sector interest)
    """
    cost = project_cost
    if not cost and opportunity_id:
        biz = get_business_by_id(opportunity_id)
        if biz:
            cost = biz.requirements.recommended_capital
    if not cost:
        cost = 150000.0

    category = opportunity_id or "all"
    
    # Construct UserProfile if user parameters are provided
    user_profile = None
    if any([user_capital, primary_skill, sector_interest, district, state]):
        user_profile = UserProfile(
            skills=[primary_skill] if primary_skill else [],
            capital=user_capital or 0.0,
            resources=[],
            interests=[sector_interest] if sector_interest else [],
            location={"district": district or "Wardha", "state": state or "Maharashtra"}
        )

    return match_schemes(user_profile=user_profile, project_cost=cost, business_category=category)


@router.get("/by-opportunity/{opportunity_id}", response_model=List[SchemeMatchItem])
def get_schemes_for_opportunity(opportunity_id: str):
    """
    Returns tailored government schemes for a specific business opportunity ID,
    automatically calibrated to the opportunity's standard capex.
    """
    biz = get_business_by_id(opportunity_id)
    cost = biz.requirements.recommended_capital if biz else 150000.0
    return match_schemes(user_profile=None, project_cost=cost, business_category=opportunity_id)


@router.post("/matches", response_model=List[SchemeMatchItem])
def get_scheme_matches(request: SchemeMatchRequest):
    """
    Match the entrepreneur/business profile to potentially relevant official schemes.
    """
    try:
        matches = match_schemes(
            user_profile=request.user_profile,
            project_cost=request.project_cost,
            business_category=request.business_category
        )
        return matches
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
