from app.common.filters.filters import BaseFilter, UUIDFilter, StringFilter


class PaymentFilter(BaseFilter):
    """Фильтр - сет для платежей"""
    id: UUIDFilter | None = None
    idempotency_key: StringFilter | None = None