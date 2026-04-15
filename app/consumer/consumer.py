import structlog
from dishka import FromDishka, make_async_container
from dishka.integrations.faststream import inject, FastStreamProvider, setup_dishka
from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitMessage

from app.consumer.broker_setup import payments_queue, payments_exchange, retry_exchange_1, retry_exchange_2, \
    dlx_exchange, declare_queues
from app.domain.exceptions import PaymentHandleError
from app.domain.schemas.payments import PaymentPayload
from app.infrastructure.ioc import ApplicationProvider
from app.infrastructure.providers.rabbit_broker import RabbitProvider
from app.services.interfaces import IProcessingPaymentService
from app.settings.settings import settings, Settings, PostgresSettings, AppSettings, RabbitSettings

logger = structlog.get_logger(__name__)

broker = RabbitBroker(settings.rabbit.url)


@broker.subscriber(payments_queue, exchange=payments_exchange)
@inject
async def handle_payment_processing(
        event: PaymentPayload,
        msg: RabbitMessage,
        service: FromDishka[IProcessingPaymentService]
):
    headers = msg.headers or {}
    deaths = headers.get("x-death") or []
    retry_count = sum(d.get("count", 0) for d in deaths)
    try:
        await service.handle(event)

    except PaymentHandleError:
        event.retry_count += 1
        logger.warning(
            "Attempt failed",
            payment_id=str(event.payment_id),
            next_retry=retry_count
        )


        if retry_count == 1:

            await broker.publish(
                event,
                exchange=retry_exchange_1,
                routing_key="payments.retry.1"
            )
        elif retry_count == 2:

            await broker.publish(
                event,
                exchange=retry_exchange_2,
                routing_key="payments.retry.2"
            )
        else:

            logger.error("Max retries reached", payment_id=str(event.payment_id))
            await broker.publish(
                event,
                exchange=dlx_exchange,
                routing_key="payments.dead"
            )

def get_faststream_app(broker: RabbitBroker) -> FastStream:
    app = FastStream(broker)
    container = make_async_container(
        ApplicationProvider(),
        FastStreamProvider(),
        RabbitProvider(),
        context={
            Settings: settings,
            PostgresSettings: settings.database,
            AppSettings: settings.app,
            RabbitSettings: settings.rabbit
        }
    )
    setup_dishka(container=container, broker=broker)

    @app.after_startup
    async def setup_broker():
        await declare_queues(broker)

    return app


app = get_faststream_app(broker)
