import uuid

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Header, Security

from app.api.middlewares.authentication import api_key_scheme
from app.api.v1.requests.payments import CreatePaymentRequest
from app.api.v1.responses.payments import PaymentCreatedResponse
from app.domain.schemas.payments import PaymentDTO
from app.services.interfaces import IPaymentService

router = APIRouter(prefix="/payments", tags=["Платежи"], dependencies=[Security(api_key_scheme)],)

@router.post("",   status_code=202)
@inject
async def creat_payment(
        body: CreatePaymentRequest,
        service: FromDishka[IPaymentService],
        idempotency_key: str = Header(..., alias="Idempotency-Key"),
) -> PaymentCreatedResponse:
    """Создание платежа"""
    payment = await service.create_payment(body, idempotency_key)
    return PaymentCreatedResponse.model_validate(payment.model_dump())


@router.get("/{payment_id}", status_code=200)
@inject
async def get_payment(
    payment_id: uuid.UUID,
    service: FromDishka[IPaymentService],
) -> PaymentDTO:
    """Получение информации о платеже по ID."""
    return await service.get_payment(payment_id)
