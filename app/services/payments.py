import uuid

import structlog

from app.api.v1.requests.payments import CreatePaymentRequest
from app.common.exceptions.exceptions import NotFoundError
from app.common.filters.filters import StringFilter, UUIDFilter
from app.domain.enums import PaymentStatus
from app.domain.filters.payments import PaymentFilter
from app.domain.schemas.outbox import CreateOutboxDTO
from app.domain.schemas.payments import PaymentDTO, CreatePaymentDTO
from app.infrastructure.unit_of_work.interfaces import IUnitOfWork
from app.services.interfaces import IPaymentService

logger = structlog.getLogger(__name__)


class PaymentService(IPaymentService):
    """Сервис платежей"""

    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def create_payment(self, payment: CreatePaymentRequest, idempotency_key: str) -> PaymentDTO:
        """Создание платежа и outbox_message"""
        async with self.uow:
            try:
                existing = await self.uow.payments.get_one(filters=PaymentFilter(idempotency_key=StringFilter(eq=idempotency_key)))
                logger.info(f"Payment with key {idempotency_key}  exists: {existing.id}")
                return existing
            except NotFoundError:
                new_payment = CreatePaymentDTO(
                    id=uuid.uuid4(),
                    webhook_url=payment.webhook_url,
                    idempotency_key=idempotency_key,
                    amount=payment.amount,
                    currency=payment.currency,
                    payment_metadata=payment.payment_metadata,
                    status=PaymentStatus.PENDING,
                )
                outbox = CreateOutboxDTO(
                    id=uuid.uuid4(),
                    event_type="payment.new",
                    aggregate_id=new_payment.id,
                    payload={
                    "payment_id": str(new_payment.id),
                    "amount": str(payment.amount),
                    "currency": payment.currency,
                    "description": payment.description,
                    "webhook_url": payment.webhook_url,
                },
                    attempts=0
                )
                payment = await self.uow.payments.create(new_payment)
                logger.info(
                    "Платёж создан",
                    payment_id=str(new_payment.id),
                    amount=str(payment.amount),
                    currency=payment.currency,
                )
                await self.uow.outbox.create(outbox)
                await self.uow.commit()
                return payment

    async def get_payment(self, payment_id: uuid.UUID) -> PaymentDTO:
        """Получение платежа"""
        async with self.uow:
            return await self.uow.payments.get_one(filters=PaymentFilter(id=UUIDFilter(eq=payment_id)))

