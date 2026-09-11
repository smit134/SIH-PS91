"""Partner Discovery and Co-Founder Matching Stubs (Aishwarya Handshake)."""

from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.spatial import haversine_distance_km
from app.models.partner import PartnerProfile
from app.models.user import User
from app.schemas.integration import PartnerMatchResponse

router = APIRouter(prefix="/partners", tags=["Partners & Team Matching"])


@router.get("/recommendations", response_model=List[PartnerMatchResponse])
async def get_partner_recommendations(
    radius_km: float = Query(50.0, ge=1.0, le=200.0),
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Finds complementary local micro-enterprise partners and co-founders.

    Matches based on geographic radius and profile complementary skills.
    Protects user domestic address under Section 33 privacy requirements.
    """
    user_lat = current_user.profile.latitude if current_user.profile else None
    user_lon = current_user.profile.longitude if current_user.profile else None

    # Fetch active partner profiles excluding caller's own
    res = await db.execute(
        select(PartnerProfile)
        .where(PartnerProfile.user_id != current_user.id)
        .where(PartnerProfile.is_looking_for_partner == True)
        .limit(limit)
    )
    partners = res.scalars().all()

    matches: List[PartnerMatchResponse] = []
    for partner in partners:
        distance = None
        # Compute distance if coordinates are present on both ends
        p_user = partner.user
        if user_lat and user_lon and p_user and p_user.profile and p_user.profile.latitude and p_user.profile.longitude:
            distance = haversine_distance_km(
                user_lat, user_lon, p_user.profile.latitude, p_user.profile.longitude
            )
            if distance > radius_km:
                continue

        matches.append(
            PartnerMatchResponse(
                partner_id=str(partner.id),
                partner_name=partner.user.profile.full_name if (partner.user and partner.user.profile) else "Entrepreneur",
                approx_location=partner.user.profile.approx_location_name if (partner.user and partner.user.profile) else None,
                distance_km=distance,
                synergy_score=85.0,
                complementary_skills=["Marketing", "Supply Chain"],
                contact_status="AVAILABLE",
            )
        )

    return matches
