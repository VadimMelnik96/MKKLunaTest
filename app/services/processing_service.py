import datetime

import structlog
from faststream.rabbit import RabbitBroker


from app.common.filters.filters import UUIDFilter
from app.domain.enums import PaymentStatus
from app.domain.exceptions import GatewayNetworkError, WebhookError, PaymentHandleError
from app.domain.filters.payments import PaymentFilter
from app.domain.schemas.gateway_results import GatewayResult
from app.domain.schemas.payments import PaymentPayload, UpdatePaymentDTO, PaymentDTO
from app.infrastructure.adapters.interfaces import IPaymentGatewayAdapter, IWebhookAdapter
from app.infrastructure.unit_of_work.interfaces import IUnitOfWork
from app.services.interfaces import IProcessingPaymentService

logger = structlog.get_logger(__name__)

class ProcessingPaymentService(IProcessingPaymentService):
    """Сервис обработки платежей"""

    def __init__(self, broker: RabbitBroker, uow: IUnitOfWork, gateway_adapter: IPaymentGatewayAdapter, webhook_adapter: IWebhookAdapter):
        self.broker = broker
        self.uow = uow
        self.gateway_adapter = gateway_adapter
        self.webhook_adapter = webhook_adapter

    async def _process_payment(self, event: PaymentPayload):
        """Процесс обработки шлюзо"""
        async with self.uow:
            logger.info("Processing payment", payment_id=str(event.payment_id))

            payment = await self.uow.payments.get_one(filters=PaymentFilter(id=UUIDFilter(eq=event.payment_id)))

            if payment.status in (PaymentStatus.SUCCEEDED, PaymentStatus.FAILED):
                logger.info(
                    "Payment already proccessed",
                    payment_id=str(payment.id),
                    status=payment.status,
                            )
                return payment
        result: GatewayResult = await self.gateway_adapter.process(
            payment_id=event.payment_id,
            amount=payment.amount,
        )
        async with self.uow:
            new_status = PaymentStatus.SUCCEEDED if result.success else PaymentStatus.FAILED
            payment = await self.uow.payments.update(
                update_dto=UpdatePaymentDTO(status=new_status, processed_at=datetime.datetime.now(datetime.UTC)),
                filters=PaymentFilter(id=UUIDFilter(eq=event.payment_id))
            )
            return payment


    async def _process_webhook(self, event: PaymentDTO) -> bool:
        """Обработка вебхука"""
        return await self.webhook_adapter.send(event.webhook_url, event.model_dump())


    async def handle(self, event: PaymentPayload) -> PaymentDTO:
        """Обработка платежа"""
        try:
            payment = await self._process_payment(event)
        except GatewayNetworkError as e:
            logger.error("Gateway network error", error=str(e))
            raise PaymentHandleError()
        try:
            await self._process_webhook(payment)
        except WebhookError as e:
            logger.error("Webhook error", error=str(e))
            raise PaymentHandleError()
        return payment




