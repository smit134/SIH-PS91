from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.models.financials import UserProfile, SchemeMatchItem
from app.services.scheme_engine import match_schemes

router = APIRouter(
    prefix="/schemes",
    tags=["schemes"]
)

class SchemeMatchRequest(BaseModel):
    user_profile: UserProfile
    project_cost: float
    business_category: str

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
