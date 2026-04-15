import abc
import uuid

from app.api.v1.requests.payments import CreatePaymentRequest
from app.domain.schemas.payments import PaymentDTO, PaymentPayload


class IPaymentService(abc.ABC):
    """Интерфейс сервиса платежей"""
    @abc.abstractmethod
    async def create_payment(self, payment: CreatePaymentRequest, idempotency_key: str) -> PaymentDTO:
        """Создание платежа"""

    @abc.abstractmethod
    async def get_payment(self, payment_id: uuid.UUID):
        """Получение платежа"""


class IOutboxService(abc.ABC):
    """Интерфейс сервиса Outbox"""

    @abc.abstractmethod
    async def publish_pending(self):
        """Публикация сообщений о платежах"""


class IProcessingPaymentService(abc.ABC):
    """Сервис для обработки платежей"""

    @abc.abstractmethod
    async def handle(self, event: PaymentPayload) -> PaymentDTO:
        """Обработка платежа"""


class IFloodPaymentsTestService(abc.ABC):
    """Сервис для наводнения платежами """

    @abc.abstractmethod
    async def flood(self, amount: int) -> None:
        """Генерирует несколько фейковых платежей и отсылает их """
