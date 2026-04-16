import asyncio
import random
from decimal import Decimal
from uuid import UUID

import structlog

from app.domain.exceptions import GatewayNetworkError
from app.domain.schemas.gateway_results import GatewayResult
from app.infrastructure.adapters.interfaces import IPaymentGatewayAdapter

logger = structlog.get_logger(__name__)


class PaymentGatewayAdapter(IPaymentGatewayAdapter):
    """Имитация платежного шлюза"""

    async def process(self, payment_id: UUID, amount: Decimal) -> GatewayResult:
        """Имитация отправки на шлюз"""
        logger.info(
            f"Посылаем платеж {payment_id} стоимостью {amount}"
        )

        await asyncio.sleep(random.randint(2, 5))

        if random.random() < 0.1:
            raise GatewayNetworkError(
                f"Gateway network error for payment {payment_id}"
            )

        success = random.random() < 0.9

        if success:
            return GatewayResult(
                success=True,
                error_message=None,
            )

        return GatewayResult(
            success=False,
            error_message="Payment declined",
        )

