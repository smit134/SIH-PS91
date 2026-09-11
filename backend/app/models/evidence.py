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
"""Hyper-Local Evidence and Reliability Classification Models."""

from datetime import datetime, timezone
import enum
from typing import Any, Dict, Optional
from sqlalchemy import DateTime, Enum, Float, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class EvidenceReliabilityClass(str, enum.Enum):
    """Reliability classifications strictly mandated by ThinkForge specification."""

    VERIFIED = "VERIFIED"    # 🟢 Directly supported by an official/primary source
    DERIVED = "DERIVED"      # 🔵 Deterministically calculated from verified inputs
    ESTIMATED = "ESTIMATED"  # 🟡 Statistical proxy or model/heuristic estimate
    UNKNOWN = "UNKNOWN"      # ⚪ Insufficient local evidence


class EvidenceType(str, enum.Enum):
    PRICE = "PRICE"
    COMPETITOR = "COMPETITOR"
    DEMAND = "DEMAND"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    DEMOGRAPHIC = "DEMOGRAPHIC"


class EvidenceRecord(Base):
    """Hyper-local signal or dataset slice with explicit confidence and provenance."""

    __tablename__ = "evidence"

    source_name: Mapped[str] = mapped_column(
        String(100),
        index=True,
        nullable=False,
        comment="Primary source (e.g., Udyam, e-NAM, Census, OpenStreetMap)",
    )
    evidence_type: Mapped[EvidenceType] = mapped_column(
        Enum(EvidenceType, name="evidence_type_enum", native_enum=False),
        index=True,
        nullable=False,
    )
    reliability_class: Mapped[EvidenceReliabilityClass] = mapped_column(
        Enum(EvidenceReliabilityClass, name="evidence_reliability_enum", native_enum=False),
        index=True,
        nullable=False,
        comment="Reliability tier: VERIFIED, DERIVED, ESTIMATED, or UNKNOWN",
    )
    confidence_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Confidence metric from 0 to 100",
    )
    latitude: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="Anchor latitude",
    )
    longitude: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="Anchor longitude",
    )
    radius_km: Mapped[Optional[float]] = mapped_column(
        Float,
        default=10.0,
        nullable=True,
        comment="Applicable geographic catchment radius in km",
    )
    payload: Mapped[Dict[str, Any]] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
        comment="Detailed signals (e.g., price points, registered enterprise counts)",
    )
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        comment="Timestamp when evidence was queried or snapshot was captured",
    )
