import datetime

import structlog
from faststream.rabbit import RabbitBroker

from app.common.database import Database
from app.common.filters.filters import BooleanFilter, NumberFilter, Condition, DateFilter, UUIDFilter
from app.domain.filters.outbox import OutboxFilter
from app.domain.schemas.outbox import UpdateOutboxDTO
from app.infrastructure.unit_of_work.uow import UnitOfWork
from app.services.interfaces import IOutboxService
from app.settings.settings import Settings

logger = structlog.get_logger(__name__)


class OutBoxService(IOutboxService):
    """Сервис outbox"""

    def __init__(self, broker: RabbitBroker, db: Database, settings: Settings):
        self.db = db
        self.broker = broker
        self.settings = settings

    def _make_uow(self) -> UnitOfWork:
        """Инициализация единицы работы для другого Scope"""
        return UnitOfWork(db=self.db)

    async def publish_pending(self):
        """Публикация outbox"""
        uow = self._make_uow()
        logger.info("Запуск публикации outbox messages")
        async with uow:
            outbox_messages = await uow.outbox.get_list(
                filters=OutboxFilter(
                    condition=Condition.AND,
                    attempts=NumberFilter(lt=self.settings.outbox.max_attempts),
                    published_at=DateFilter(eq=None)
                )
            )
            if not outbox_messages:
                logger.info("Нет сообщений для отправки")
                return

            for message in outbox_messages:
                    try:
                        await self.broker.publish(
                            message=message.payload,
                            routing_key=message.event_type,
                            exchange=self.settings.outbox.exchange
                        )
                        await uow.outbox.update(
                            UpdateOutboxDTO(
                                published_at=datetime.datetime.now(tz=datetime.timezone.utc),
                                attempts=message.attempts + 1,
                            ),
                            filters=OutboxFilter(id=UUIDFilter(eq=message.id))
                        )
                    except Exception as e:
                        logger.warning(
                            "Ошибка публикации outbox-сообщения",
                            outbox_id=str(message.id),
                            attempts=message.attempts,
                            error=str(e),
                        )
                        attempts = message.attempts + 1
                        await uow.outbox.update(
                                UpdateOutboxDTO(
                                    attempts=attempts,
                                ),
                                filters=OutboxFilter(id=UUIDFilter(eq=message.id))
                            )
            await uow.commit()
        logger.info("Отправка outbox messages завершена")
