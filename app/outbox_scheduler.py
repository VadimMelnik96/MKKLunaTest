import asyncio

import structlog
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dishka import make_async_container

from app.infrastructure.ioc import ApplicationProvider
from app.infrastructure.providers.rabbit_broker import RabbitProvider
from app.services.interfaces import IOutboxService
from app.settings.settings import AppSettings, PostgresSettings, RabbitSettings, Settings, settings

logger = structlog.get_logger()


async def main() -> None:
    """Запуск планировщика задач"""
    container = make_async_container(
        ApplicationProvider(),

        RabbitProvider(),
        context={
            Settings: settings,
            PostgresSettings: settings.database,
            AppSettings: settings.app,
            RabbitSettings: settings.rabbit
        }
    )

    try:
        async with container() as request_container:
           service = await request_container.get(IOutboxService)
           logger.info(f"Получили сервис из контейнера {type(service)}")
    except Exception as e:
        logger.info(f"Ошибка инициализации контейнера {e}")
        raise

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        service.publish_pending,
        "interval",
        seconds=settings.outbox.frequency
    )
    scheduler.start()
    logger.info("Планировщик запущен")
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Остановка планировщика")
        scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
