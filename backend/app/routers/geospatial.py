"""
FastAPI Router for Geospatial Proximity & Local Evidence Layer (Part 4 - Aishwarya).
Endpoints for local opportunity snapshots, MSME competitor density, and POI queries.
"""

from typing import List, Optional
from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.database import get_db
from ..models.evidence import (
    LocalOpportunitySnapshot,
    RegisteredMSMEItem,
    POIItem,
)
from ..engines.geospatial_engine import GeospatialEngine
from ..data.sample_evidence import SAMPLE_REGIONAL_PRICES


router = APIRouter(prefix="/api/intelligence/geospatial", tags=["Geospatial & Local Evidence Layer"])


@router.get("/evidence-snapshot", response_model=LocalOpportunitySnapshot, summary="Get comprehensive local evidence snapshot")
async def get_local_evidence_snapshot(
    latitude: float = Query(..., description="Latitude coordinate", ge=-90.0, le=90.0),
    longitude: float = Query(..., description="Longitude coordinate", ge=-180.0, le=180.0),
    radius_km: float = Query(default=10.0, description="Service radius in km", ge=1.0, le=50.0),
    category: Optional[str] = Query(default=None, description="Optional business category filter"),
    db: AsyncSession = Depends(get_db)
):
    """
    Computes local opportunity score, market signals, registered MSME count,
    POI infrastructure, and evidence coverage breakdown with provenance.
    """
    return await GeospatialEngine.evaluate_local_signals(
        session=db,
        lat=latitude,
        lon=longitude,
        radius_km=radius_km,
        category=category
    )


@router.get("/nearby-msmes", response_model=List[RegisteredMSMEItem], summary="Get nearby registered MSMEs within radius")
async def get_nearby_msmes(
    latitude: float = Query(..., description="Latitude coordinate"),
    longitude: float = Query(..., description="Longitude coordinate"),
    radius_km: float = Query(default=10.0, description="Radius in km"),
    category: Optional[str] = Query(default=None, description="Category filter"),
    db: AsyncSession = Depends(get_db)
):
    """Queries registered MSMEs from available registry with computed distances."""
    return await GeospatialEngine.get_nearby_msmes(
        session=db,
        lat=latitude,
        lon=longitude,
        radius_km=radius_km,
        category=category
    )


@router.get("/nearby-pois", response_model=List[POIItem], summary="Get local POIs within radius")
async def get_nearby_pois(
    latitude: float = Query(..., description="Latitude coordinate"),
    longitude: float = Query(..., description="Longitude coordinate"),
    radius_km: float = Query(default=10.0, description="Radius in km"),
    db: AsyncSession = Depends(get_db)
):
    """Queries local infrastructure POIs (Mandis, Haats, Banks, Transport hubs) within radius."""
    return await GeospatialEngine.get_nearby_pois(
        session=db,
        lat=latitude,
        lon=longitude,
        radius_km=radius_km
    )


@router.get("/regional-prices", summary="Get benchmark regional commodity & product price references")
async def get_regional_prices(
    category: Optional[str] = Query(default=None, description="Business category id")
):
    """Returns official/proxy regional price references with data sources."""
    if category and category in SAMPLE_REGIONAL_PRICES:
        return {category: SAMPLE_REGIONAL_PRICES[category]}
    return SAMPLE_REGIONAL_PRICES
