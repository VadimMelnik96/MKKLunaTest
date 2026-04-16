import abc

from app.common.repositories.interfaces import IRepository


class IOutboxRepo(IRepository, abc.ABC):
    """Интерфейс репо outbox"""


class IPaymentsRepo(IRepository, abc.ABC):
    """Интерфейс репо платежей"""
