import uuid

import httpx
from faker import Faker

from app.api.v1.requests.payments import CreatePaymentRequest
from app.domain.enums import CurrencyEnum
from app.services.interfaces import IFloodPaymentsTestService
from app.settings.settings import settings

fake = Faker()

class FloodPaymentTestService(IFloodPaymentsTestService):
    """Наводнение платежами api"""

    async def flood(self, amount: int) -> None:
        """Тестовый метод наводнения платежами"""
        currencies = [CurrencyEnum.RUB, CurrencyEnum.USD, CurrencyEnum.EUR]
        async with httpx.AsyncClient() as client:
            for _ in range(amount):
                idempotency_key = str(uuid.uuid4())
                body = CreatePaymentRequest(
                        amount=fake.pyfloat(left_digits=4, right_digits=2, positive=True),
                        currency=fake.random_element(currencies),
                        description=fake.sentence(nb_words=4),
                        payment_metadata={
                            "order_id": str(uuid.uuid4()),
                            "customer": fake.name(),
                            "email": fake.email(),
                        },
                        webhook_url=fake.url(),
                    )

                resp = await client.post(url="http://localhost:8000/payments", json=body.model_dump(), headers={"X-Api-Key": settings.app.static_api_key, "Idempotency-Key": idempotency_key})



