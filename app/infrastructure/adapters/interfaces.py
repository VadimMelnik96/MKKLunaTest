import abc
from decimal import Decimal
from uuid import UUID

from app.domain.schemas.gateway_results import GatewayResult


class IWebhookAdapter(abc.ABC):
    """Интерфейс адаптера вебхука"""

    @abc.abstractmethod
    async def send(self, url: str, payload: dict) -> None:
       """Метод отправки информации на вебхук"""


class IPaymentGatewayAdapter(abc.ABC):
    """Адаптер для шлюза"""

    @abc.abstractmethod
    async def process(self, payment_id: UUID, amount: Decimal) -> GatewayResult:
        """Отправка платежа"""
