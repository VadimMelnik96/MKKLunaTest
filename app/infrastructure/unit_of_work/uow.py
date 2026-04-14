from app.common.uow.base_uow import BaseUnitOfWork
from app.domain.repositories.outbox import OutboxRepo
from app.domain.repositories.payments import PaymentsRepo
from app.infrastructure.unit_of_work.interfaces import IUnitOfWork


class UnitOfWork(BaseUnitOfWork, IUnitOfWork):
    """Единица работы"""

    async def __aenter__(self) -> None:
        """Инициализация сессии и репозиториев."""
        await super().__aenter__()
        self.payments = PaymentsRepo(session=self.session)
        self.outbox = OutboxRepo(session=self.session)