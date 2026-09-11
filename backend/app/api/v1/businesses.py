"""Business Category Recommendations and Feasibility Stubs (Aishwarya Handshake)."""

from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.business import BusinessCategory
from app.models.user import User
from app.schemas.integration import BusinessRecommendationResponse

router = APIRouter(prefix="/businesses", tags=["Businesses & Recommendations"])


@router.get("/recommendations", response_model=List[BusinessRecommendationResponse])
async def get_business_recommendations(
    limit: int = Query(5, ge=1, le=20),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Provides prioritized rural business opportunity recommendations for the entrepreneur.

    Interprets user's capability profile, working capital, and benchmark business categories.
    Handshake contract for Aishwarya's AI Feasibility Engine.
    """
    user_capital = current_user.profile.available_capital if current_user.profile else 0
    res = await db.execute(select(BusinessCategory).limit(limit))
    categories = res.scalars().all()

    recommendations: List[BusinessRecommendationResponse] = []
    for cat in categories:
        # Feasibility heuristics based on capital coverage
        if user_capital >= cat.min_capital:
            score = 88.0
            rationale = f"Your working capital (Rs. {user_capital:,}) meets or exceeds the baseline threshold (Rs. {cat.min_capital:,})."
        elif user_capital >= (cat.min_capital * 0.5):
            score = 65.0
            rationale = f"Moderate fit. Additional micro-credit or subsidy recommended to bridge capital gap of Rs. {cat.min_capital - user_capital:,}."
        else:
            score = 45.0
            rationale = f"High capital gap. Government scheme subsidy or co-founder partnership advised."

        recommendations.append(
            BusinessRecommendationResponse(
                category_code=cat.code,
                category_name=cat.name,
                feasibility_score=score,
                risk_level=cat.risk_level,
                capital_required=cat.min_capital,
                break_even_months=cat.break_even_months_est,
                rationale=rationale,
                key_drivers=[
                    f"Min capital: Rs. {cat.min_capital:,}",
                    f"Break-even: ~{cat.break_even_months_est} months",
                ],
            )
        )

    # Sort descending by feasibility score
    recommendations.sort(key=lambda r: r.feasibility_score, reverse=True)
    return recommendations
