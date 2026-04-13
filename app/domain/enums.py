import enum


class PaymentStatus(str, enum.Enum):
    """Статусы платежей"""
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class CurrencyEnum(str, enum.Enum):
    """Валюты для платежей"""
    USD = "USD"
    RUB = "RUB"
    EUR = "EUR"
