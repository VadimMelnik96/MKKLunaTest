import uuid
from datetime import datetime

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import mapped_column, Mapped

from app.infrastructure.models.base import Base
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, JSONB


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