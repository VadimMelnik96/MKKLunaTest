import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Numeric, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.enums import PaymentStatus, CurrencyEnum
from app.infrastructure.models.base import Base
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP


class Payment(Base):
    __tablename__ = 'payments'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(String(40), nullable=False)
    description: Mapped[String] = mapped_column(String(255), nullable=True)
    payment_metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    currency: Mapped[CurrencyEnum] = mapped_column(String, nullable=True)
    webhook_url: Mapped[str] = mapped_column(String(500), nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(500), nullable=False)
    processed_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)