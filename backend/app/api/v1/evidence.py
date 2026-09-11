"""Field Evidence and Hyper-Local Ground Truth Stubs (Smit Handshake)."""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.spatial import haversine_distance_km
from app.models.evidence import EvidenceRecord
from app.models.user import User
from app.schemas.integration import EvidenceNearbyResponse

router = APIRouter(prefix="/evidence", tags=["Field Evidence & Ground Truth"])


@router.get("/nearby", response_model=List[EvidenceNearbyResponse])
async def get_nearby_field_evidence(
    radius_km: float = Query(50.0, ge=1.0, le=200.0),
    reliability: Optional[str] = Query(None, description="VERIFIED, DERIVED, ESTIMATED, UNKNOWN"),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieves local ground-truth evidence records (market rates, demand proxies, competitor density).

    Guarantees Section 33 reliability class enforcement (VERIFIED, DERIVED, ESTIMATED, UNKNOWN).
    Handshake contract for Smit's Ground Truth Engine.
    """
    query = select(EvidenceRecord)
    if reliability:
        query = query.where(EvidenceRecord.reliability_class == reliability.upper())

    query = query.limit(limit)
    res = await db.execute(query)
    records = res.scalars().all()

    user_lat = current_user.profile.latitude if current_user.profile else None
    user_lon = current_user.profile.longitude if current_user.profile else None

    results: List[EvidenceNearbyResponse] = []
    for rec in records:
        distance = None
        if user_lat and user_lon and rec.latitude and rec.longitude:
            distance = haversine_distance_km(user_lat, user_lon, rec.latitude, rec.longitude)
            if distance > radius_km:
                continue

        results.append(
            EvidenceNearbyResponse(
                evidence_id=str(rec.id),
                source_name=rec.source_name,
                evidence_type=rec.evidence_type.value if hasattr(rec.evidence_type, "value") else str(rec.evidence_type),
                reliability_class=rec.reliability_class.value if hasattr(rec.reliability_class, "value") else str(rec.reliability_class),
                confidence_score=rec.confidence_score,
                payload=rec.payload,
                distance_km=distance,
                fetched_at=rec.fetched_at,
            )
        )

    return results

