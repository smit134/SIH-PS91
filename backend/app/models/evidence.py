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
