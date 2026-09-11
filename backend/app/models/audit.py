"""System Audit Log Model for Security and Privacy Lineage."""

import uuid
from typing import TYPE_CHECKING, Any, Dict, Optional
from sqlalchemy import ForeignKey, JSON, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class AuditLog(Base):
    """Audit log tracking sensitive operations, authentication events, and consent handshakes."""

    __tablename__ = "audit_logs"

    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    action: Mapped[str] = mapped_column(
        String(100),
        index=True,
        nullable=False,
        comment="Event type (e.g. AUTH_LOGIN, CONSENT_GRANTED, PROFILE_UPDATED)",
    )
    resource_type: Mapped[str] = mapped_column(
        String(50),
        index=True,
        nullable=False,
        comment="Target resource category (e.g. USER, PROFILE, PARTNER_MATCH)",
    )
    resource_id: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="ID of the entity affected",
    )
    ip_address: Mapped[Optional[str]] = mapped_column(
        String(45),
        nullable=True,
        comment="Client IP address",
    )
    details: Mapped[Dict[str, Any]] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
        comment="Structured metadata describing the event",
    )

    user: Mapped[Optional["User"]] = relationship("User", back_populates="audit_logs")
