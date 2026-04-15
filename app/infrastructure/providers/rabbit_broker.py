from collections.abc import AsyncGenerator

from dishka import Provider, Scope, provide
from faststream.rabbit import RabbitBroker

from app.settings.settings import RabbitSettings


class RabbitProvider(Provider):
    """Провайдер RabbitMQ брокера"""

    @provide(scope=Scope.APP)
    async def get_broker(self, settings: RabbitSettings) -> AsyncGenerator[RabbitBroker, None]:
        broker = RabbitBroker(settings.url)
        await broker.connect()
        try:
            yield broker
        finally:
            await broker.stop()