import uuid
from datetime import datetime

from app.common.arbitrary_model import ArbitraryModel


class CreateOutboxDTO(ArbitraryModel):
    """Создание аутбокс"""
    id: uuid.UUID
    event_type: str
    aggregate_id: uuid.UUID
    payload: dict
    attempts: int
    published_at: datetime | None = None
    is_dead: bool = False


class OutboxDTO(CreateOutboxDTO):
    """Аутбокс ДТО"""
    created_at: datetime | None = None
    updated_at: datetime | None = None
