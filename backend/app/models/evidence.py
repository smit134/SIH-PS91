"""
Local Evidence, Geospatial POIs, MSME Density, and Evidence Classification Models (Section 10, 14, 18, 45, 46).
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .common import EvidenceClass


class RegisteredMSMEItem(BaseModel):
    """Registered Enterprise in Udyam / Local Registry (Section 10, 46)"""
    enterprise_id: str
    name: str
    category: str
    latitude: float
    longitude: float
    distance_km: Optional[float] = None
    source: str = Field(default="Udyam MSME Registry (Mock Sample)")
    registration_year: int = Field(default=2023)


class POIItem(BaseModel):
    """Local Point of Interest (Market, Mandi, Transport Hub, Cold Storage)"""
    poi_id: str
    name: str
    poi_type: str = Field(..., description="e.g. 'Mandi', 'Weekly Haat', 'Railway Station', 'Cooperative Bank'")
    latitude: float
    longitude: float
    distance_km: Optional[float] = None


class LocalEvidenceItem(BaseModel):
    """Individual Local Evidence Metric with Provenance & Limitation (Section 18, 45)"""
    metric_name: str
    value_display: str
    score: float = Field(..., description="0-100 score for this indicator", ge=0.0, le=100.0)
    evidence_class: EvidenceClass
    source: str
    retrieval_date: str = Field(default="2026-03-01")
    limitation_note: str


class LocalOpportunitySnapshot(BaseModel):
    """
    Hyper-Local Opportunity Intelligence Snapshot (Section 10 & 14).
    Calculated strictly from deterministic geospatial queries and evidence coverage rules.
    """
    service_radius_km: float
    latitude: float
    longitude: float
    
    # Aggregated Signals (0-100)
    market_signal_score: float
    competition_pressure_score: float
    price_signal_score: float
    resource_availability_score: float
    local_opportunity_composite: float
    
    # Evidence Coverage (Section 18)
    overall_evidence_coverage_percentage: float
    coverage_breakdown: List[LocalEvidenceItem]
    
    # Geospatial Counts
    registered_enterprises_found: int
    registry_disclaimer: str = Field(
        default="Registered enterprises found in available registry. Does not represent a total census of unregistered micro-units."
    )
    relevant_pois: List[POIItem]
    competitor_sample: List[RegisteredMSMEItem]
