"""User Interaction Model for AI Recommendations."""

import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class InteractionType(str, enum.Enum):
    LIKE = "LIKE"
    DISLIKE = "DISLIKE"
    VIEW = "VIEW"


class UserInteraction(Base):
    """Stores a user's interaction with a specific business opportunity."""

    __tablename__ = "user_interactions"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    user_id: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )
    business_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="The ID of the business category from the catalog",
    )
    interaction_type: Mapped[InteractionType] = mapped_column(
        Enum(InteractionType, name="interaction_type_enum", native_enum=False),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )


