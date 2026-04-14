from app.common.repositories.repository import SQLAlchemyRepository
from app.domain.repositories.interfaces import IOutboxRepo
from app.domain.schemas.outbox import OutboxDTO
from app.infrastructure.models.outbox import OutboxMessage


class OutboxRepo(SQLAlchemyRepository, IOutboxRepo):
    """Репо outbox"""
    model = OutboxMessage
    response_dto = OutboxDTO
