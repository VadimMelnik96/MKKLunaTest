import structlog
from dishka import FromDishka, make_async_container
from dishka.integrations.faststream import FastStreamProvider, inject, setup_dishka
from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitMessage

from app.consumer.broker_setup import (
    declare_queues,
    payments_exchange,
    payments_queue,
    retry_exchange_1,
    retry_exchange_2,
)
from app.domain.exceptions import PaymentHandleError
from app.domain.schemas.payments import PaymentPayload
from app.infrastructure.ioc import ApplicationProvider
from app.infrastructure.providers.rabbit_broker import RabbitProvider
from app.services.interfaces import IProcessingPaymentService
from app.settings.settings import AppSettings, PostgresSettings, RabbitSettings, Settings, settings

logger = structlog.get_logger(__name__)

broker = RabbitBroker(settings.rabbit.url)

def _get_retry_count(msg: RabbitMessage) -> int:
    """Утилита подсчета заголовков"""
    headers = msg.headers or {}
    custom = headers.get("x-retry-attempt")
    if custom is not None:
        return int(custom)
    deaths = headers.get("x-death") or []
    return sum(d.get("count", 0) for d in deaths)


@broker.subscriber(payments_queue, exchange=payments_exchange, no_ack=True)
@inject
async def handle_payment_processing(
        event: PaymentPayload,
        msg: RabbitMessage,
        service: FromDishka[IProcessingPaymentService]
) -> None:
    """Обработка платежа"""
    retry_count = _get_retry_count(msg)

    logger.info(
        "Получено событие payment.new",
        payment_id=str(event.payment_id),
        retry_count=retry_count,
    )

    try:
        await service.handle(event)
        await msg.ack()
        logger.info("Платёж успешно обработан", payment_id=str(event.payment_id))

    except PaymentHandleError as exc:
        logger.warning(
            "Ошибка обработки платежа",
            payment_id=str(event.payment_id),
            retry_count=retry_count,
            error=str(exc),
        )

        next_attempt = retry_count + 1

        if next_attempt > 2:
            logger.error(
                "Платёж отправлен в DLQ",
                payment_id=str(event.payment_id),
                total_attempts=retry_count + 1,
            )
            await msg.nack(requeue=False)
            return


        retry_exchange = retry_exchange_1 if next_attempt == 1 else retry_exchange_2
        retry_routing_key = f"payments.retry.{next_attempt}"

        try:
            await broker.publish(
                message=event,
                exchange=retry_exchange,
                routing_key=retry_routing_key,
                headers={
                    **(msg.headers or {}),
                    "x-retry-attempt": next_attempt,
                },
            )
            logger.info(
                "Платёж отправлен в retry-очередь",
                payment_id=str(event.payment_id),
                routing_key=retry_routing_key,
                delay_seconds=5 if next_attempt == 1 else 15,
            )
            await msg.ack()  # ack оригинала — копия уже в retry с TTL

        except Exception as publish_exc:
            logger.error(
                "Не удалось опубликовать в retry, nack → DLQ",
                payment_id=str(event.payment_id),
                error=str(publish_exc),
            )
            await msg.nack(requeue=False)


def get_faststream_app(broker: RabbitBroker) -> FastStream:
    """Настройка Faststream приложения"""
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
    async def setup_broker() -> None:
        await declare_queues(broker)

    return app


app = get_faststream_app(broker)
