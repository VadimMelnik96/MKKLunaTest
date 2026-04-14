from dishka import Provider, from_context, Scope, provide

from app.common.database import Database
from app.infrastructure.unit_of_work.interfaces import IUnitOfWork
from app.infrastructure.unit_of_work.uow import UnitOfWork
from app.services.interfaces import IPaymentService
from app.services.payments import PaymentService
from app.settings.settings import Settings, PostgresSettings, AppSettings


class ApplicationProvider(Provider):
    """Провайдер зависимостей"""
    settings = from_context(provides=Settings, scope=Scope.APP)
    postgres_config = from_context(provides=PostgresSettings, scope=Scope.APP)
    app_config = from_context(provides=AppSettings, scope=Scope.APP)
    database = provide(Database, scope=Scope.APP)
    unit_of_work = provide(UnitOfWork, scope=Scope.REQUEST, provides=IUnitOfWork)
    payment_service = provide(PaymentService, scope=Scope.REQUEST, provides=IPaymentService)