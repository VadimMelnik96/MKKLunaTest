import uuid
from datetime import datetime

from app.common.arbitrary_model import ArbitraryModel
from app.domain.enums import CurrencyEnum, PaymentStatus


class CreatePaymentDTO(ArbitraryModel):
    """ДТО создания платежа"""

    id: uuid.UUID
    amount: float
    currency: CurrencyEnum
    status: PaymentStatus
    payment_metadata: dict | None = None
    description: str | None = None
    webhook_url: str
    idempotency_key: str
    processed_at: datetime | None = None


class PaymentDTO(CreatePaymentDTO):
    """ДТО для платежей"""

    created_at: datetime | None = None
    updated_at: datetime | None = None
