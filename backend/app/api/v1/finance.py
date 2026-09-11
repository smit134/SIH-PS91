"""Financial Viability Simulation and Scheme Matching Stubs (Kesha Handshake)."""

from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.scheme import GovernmentScheme
from app.models.user import User
from app.schemas.integration import (
    FinanceSimulationRequest,
    FinanceSimulationResponse,
    SchemeMatchResponse,
)

router = APIRouter(tags=["Finance & Schemes"])


@router.post("/finance/simulate", response_model=FinanceSimulationResponse)
async def simulate_financial_viability(
    payload: FinanceSimulationRequest,
    current_user: User = Depends(get_current_user),
):
    """Simulates micro-enterprise financial viability, cash runway, and break-even horizon.

    Handshake contract for Kesha's Financial Modeling Engine.
    """
    monthly_net = payload.monthly_revenue_projected - payload.monthly_expenses_projected
    profit_margin = (
        round((monthly_net / payload.monthly_revenue_projected) * 100.0, 2)
        if payload.monthly_revenue_projected > 0
        else 0.0
    )

    if monthly_net > 0:
        break_even_months = round(payload.capital_invested / monthly_net, 1)
        runway_months = 999.0  # Profitable, self-sustaining
        is_viable = True
    elif monthly_net < 0:
        burn_rate = abs(monthly_net)
        break_even_months = -1.0  # Cannot break even while cash-flow negative
        runway_months = round(payload.capital_invested / burn_rate, 1) if burn_rate > 0 else 0.0
        is_viable = False
    else:
        break_even_months = 0.0
        runway_months = 0.0
        is_viable = False

    return FinanceSimulationResponse(
        capital_invested=payload.capital_invested,
        monthly_net_profit=round(monthly_net, 2),
        profit_margin_pct=profit_margin,
        break_even_months=break_even_months,
        runway_months=runway_months,
        is_viable=is_viable,
    )


@router.get("/schemes/matches", response_model=List[SchemeMatchResponse])
async def get_matching_government_schemes(
    limit: int = Query(5, ge=1, le=20),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Identifies central and state credit-linked subsidies and loan schemes tailored for the user.

    Handshake contract for Kesha's Government Schemes Matching Engine.
    """
    res = await db.execute(
        select(GovernmentScheme)
        .where(GovernmentScheme.is_active == True)
        .limit(limit)
    )
    schemes = res.scalars().all()

    matches: List[SchemeMatchResponse] = []
    user_capital = current_user.profile.available_capital if current_user.profile else 0

    for s in schemes:
        matched_criteria = ["Age >= 18", "Rural Enterprise Category"]
        if user_capital < s.max_loan_amount:
            verdict = "HIGHLY_ELIGIBLE"
            matched_criteria.append("Working capital within financing limits")
        else:
            verdict = "ELIGIBLE"

        matches.append(
            SchemeMatchResponse(
                scheme_id=str(s.id),
                scheme_name=s.scheme_name,
                short_code=s.short_code,
                max_loan_amount=s.max_loan_amount,
                subsidy_percentage=s.subsidy_percentage,
                interest_rate_annual=s.interest_rate_annual,
                authority_name=s.authority_name,
                eligibility_verdict=verdict,
                matched_criteria=matched_criteria,
                official_source_url=s.official_source_url,
            )
        )

    return matches
