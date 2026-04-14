import abc
import uuid

from app.api.v1.requests.payments import CreatePaymentRequest
from app.domain.schemas.payments import PaymentDTO


class IPaymentService(abc.ABC):
    """Интерфейс сервиса платежей"""
    @abc.abstractmethod
    async def create_payment(self, payment: CreatePaymentRequest, idempotency_key: str) -> PaymentDTO:
        """Создание платежа"""

    @abc.abstractmethod
    async def get_payment(self, payment_id: uuid.UUID):
        """Получение платежа"""