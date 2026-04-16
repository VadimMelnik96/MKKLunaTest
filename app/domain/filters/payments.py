from app.common.filters.filters import BaseFilter, StringFilter, UUIDFilter


class PaymentFilter(BaseFilter):
    """Фильтр - сет для платежей"""
    id: UUIDFilter | None = None
    idempotency_key: StringFilter | None = None
