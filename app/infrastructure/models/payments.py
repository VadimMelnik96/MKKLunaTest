import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import JSON, Index, Numeric, String
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.enums import CurrencyEnum, PaymentStatus
from app.infrastructure.models.base import Base


class Payment(Base):
    __tablename__ = 'payments'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(String(40), nullable=False)
    description: Mapped[String] = mapped_column(String(255), nullable=True)
    payment_metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    currency: Mapped[CurrencyEnum] = mapped_column(String, nullable=True)
    webhook_url: Mapped[str] = mapped_column(String(500), nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    processed_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)

    __table_args__ = (
        Index("ix_payments_status", "status"),
        Index("ix_payments_processed_at", "processed_at"),
        Index(
            "ix_payments_status_processed",
            "status",
            "processed_at",
        ),
    )
