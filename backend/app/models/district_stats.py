"""District-wise MSME Statistics Model.

Stores district-level enterprise data from data.gov.in for
market saturation scoring in the Opportunity Engine.
"""

from typing import Any, Dict, Optional
from sqlalchemy import Float, Index, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class DistrictMSMEStats(Base):
    """District-level MSME registration and economic statistics."""

    __tablename__ = "district_msme_stats"

    district_name: Mapped[str] = mapped_column(
        String(100),
        index=True,
        nullable=False,
        comment="District name (e.g., 'Ahmedabad', 'Surat')",
    )
    state_name: Mapped[str] = mapped_column(
        String(50),
        index=True,
        nullable=False,
        comment="State name (e.g., 'Gujarat')",
    )
    total_registered_msmes: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Total registered MSMEs in district",
    )
    micro_enterprises: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Count of micro enterprises (investment < ₹1 Cr)",
    )
    small_enterprises: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Count of small enterprises (investment ₹1-10 Cr)",
    )
    medium_enterprises: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Count of medium enterprises (investment ₹10-50 Cr)",
    )
    sector_breakdown: Mapped[Dict[str, Any]] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
        comment='JSON: {"manufacturing": 450, "services": 320, "trading": 200}',
    )
    total_employment: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Total people employed across MSMEs in this district",
    )
    avg_capital_investment: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="Average capital investment per MSME in INR",
    )
    rural_enterprise_pct: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="Percentage of enterprises in rural areas (0-100)",
    )
    data_year: Mapped[int] = mapped_column(
        Integer,
        default=2023,
        nullable=False,
        comment="Year of the statistical data",
    )

    __table_args__ = (
        Index("idx_district_state", "district_name", "state_name", unique=True),
    )
