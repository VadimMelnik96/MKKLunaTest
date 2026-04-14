from app.common.arbitrary_model import ArbitraryModel
from app.domain.enums import CurrencyEnum


class CreatePaymentRequest(ArbitraryModel):
    """Создание платежа"""
    amount: float
    currency: CurrencyEnum
    description: str
    payment_metadata: dict | None = None
    webhook_url: str
