from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Security

from app.api.middlewares.authentication import api_key_scheme
from app.services.interfaces import IFloodPaymentsTestService

router = APIRouter(prefix="/test", tags=["Тестовый роутер"], dependencies=[Security(api_key_scheme)])


@router.get("/flood/{amount}")
@inject
async def flood_test(amount: int, service: FromDishka[IFloodPaymentsTestService]) -> None:
    """Роут для флуда платежей"""
    return await service.flood(amount)
