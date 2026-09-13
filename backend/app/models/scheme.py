"""Government Financing and Welfare Scheme Models."""

from typing import Any, Dict, List, Optional
from sqlalchemy import BigInteger, Boolean, Float, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class GovernmentScheme(Base):
    """Catalog of official government micro-enterprise financing schemes."""

    __tablename__ = "schemes"

    scheme_name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
        comment="Official title of the scheme",
    )
    short_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
        comment="Identifier code (e.g., PMEGP, MUDRA_KISHORE)",
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Summary of scheme objectives and support provided",
    )
    eligibility_rules: Mapped[Dict[str, Any]] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
        comment="Structured rule definitions for automated matching",
    )
    max_loan_amount: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="Ceiling financing cap in INR",
    )
    interest_rate_annual: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Base annual interest rate (e.g., 0.08 for 8%)",
    )
    subsidy_percentage: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
        comment="Government capital subsidy proportion",
    )
    tenure_months_max: Mapped[int] = mapped_column(
        Integer,
        default=60,
        nullable=False,
        comment="Maximum repayment horizon in months",
    )
    required_documents: Mapped[List[str]] = mapped_column(
        JSON,
        default=list,
        nullable=False,
        comment="List of mandatory documentation for applications",
    )
    official_source_url: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Official portal URL for verification",
    )
    authority_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Issuing ministry or nodal agency (e.g., MoSJE, KVIC, SIDBI)",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Whether the scheme is currently active for application routing",
    )

    # --- New columns for real dataset integration ---
    scheme_level: Mapped[Optional[str]] = mapped_column(
        String(20),
        default="CENTRAL",
        nullable=True,
        comment="CENTRAL or STATE level scheme",
    )
    target_state: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="Target state (NULL for central schemes)",
    )
    category_tags: Mapped[Optional[List[str]]] = mapped_column(
        JSON,
        default=list,
        nullable=True,
        comment='Category tags: ["agriculture", "msme", "women", "sc_st"]',
    )
    benefits_text: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Raw benefits description for RAG vectorization",
    )
