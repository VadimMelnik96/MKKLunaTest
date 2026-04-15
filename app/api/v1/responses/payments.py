import datetime
import uuid

from pydantic import Field

from app.common.arbitrary_model import ArbitraryModel
from app.domain.enums import PaymentStatus


class PaymentCreatedResponse(ArbitraryModel):
    """Ответ для созданного платежа"""
    payment_id: uuid.UUID = Field(alias="id")
    status: PaymentStatus
    created_at: datetime.datetime