"""Business Opportunity and Category Models."""

from typing import Any, List
from sqlalchemy import BigInteger, Boolean, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class BusinessCategory(Base):
    """Benchmarked business templates (Handicraft, Dairy, Food Processing, etc.)."""

    __tablename__ = "business_categories"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        comment="Human-readable business name",
    )
    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
        comment="Normalized business identifier code",
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Comprehensive operational description",
    )
    min_capital: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="Minimum capital threshold in INR",
    )
    max_capital: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="Upper scale capital requirement in INR",
    )
    typical_monthly_operating_cost: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="Estimated monthly raw material and labor expense in INR",
    )
    typical_monthly_revenue: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="Estimated monthly gross revenue in INR",
    )
    risk_level: Mapped[str] = mapped_column(
        String(20),
        default="MEDIUM",
        nullable=False,
        comment="Inherent risk classification (LOW, MEDIUM, HIGH)",
    )
    required_skills: Mapped[List[str]] = mapped_column(
        JSON,
        default=list,
        nullable=False,
        comment="List of essential skills needed",
    )
    required_resources: Mapped[List[str]] = mapped_column(
        JSON,
        default=list,
        nullable=False,
        comment="List of physical equipment/land types needed",
    )
    break_even_months_est: Mapped[int] = mapped_column(
        Integer,
        default=12,
        nullable=False,
        comment="Estimated timeline to achieve operational break-even",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Whether category is active in opportunity searches",
    )
