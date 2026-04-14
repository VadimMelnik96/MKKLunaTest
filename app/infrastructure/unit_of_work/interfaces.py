import abc

from app.common.uow.interfaces import BaseAbstractUnitOfWork
from app.domain.repositories.interfaces import IPaymentsRepo, IOutboxRepo


class IUnitOfWork(BaseAbstractUnitOfWork, abc.ABC):
    """Интерфейс единицы работы."""
    payments: IPaymentsRepo
    outbox: IOutboxRepo