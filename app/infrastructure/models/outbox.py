import uuid
from datetime import datetime

from sqlalchemy import Index, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.models.base import Base


class OutboxMessage(Base):
    __tablename__ = 'outbox_messages'



    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    aggregate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    published_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )

    __table_args__ = (
        Index(
            "ix_outbox_pending_only",
            "id",
            "created_at",
            postgresql_where=(published_at.is_(None)),
        ),
        Index("ix_outbox_event_type", "event_type"),
        Index("ix_outbox_attempts", "attempts"),
        Index("idx_outbox_aggregate_id", "aggregate_id"),

    )
