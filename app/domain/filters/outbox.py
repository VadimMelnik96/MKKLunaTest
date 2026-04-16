from app.common.filters.filters import BaseFilter, DateFilter, NumberFilter, StringFilter, UUIDFilter


class OutboxFilter(BaseFilter):
    """Фильтр-сет для outbox"""

    id: UUIDFilter | None = None
    event_type: StringFilter | None = None
    aggregate_id: UUIDFilter | None = None
    attempts: NumberFilter | None = None
    published_at: DateFilter | None = None
