from dishka import Provider, Scope, from_context, provide

from app.common.database import Database
from app.infrastructure.adapters.gateway_adapter import PaymentGatewayAdapter
from app.infrastructure.adapters.interfaces import IPaymentGatewayAdapter, IWebhookAdapter
from app.infrastructure.adapters.webhook_adapter import WebhookAdapter
from app.infrastructure.unit_of_work.interfaces import IUnitOfWork
from app.infrastructure.unit_of_work.uow import UnitOfWork
from app.services.flood_payment_test import FloodPaymentTestService
from app.services.interfaces import (
    IFloodPaymentsTestService,
    IOutboxService,
    IPaymentService,
    IProcessingPaymentService,
)
from app.services.outbox import OutBoxService
from app.services.payments import PaymentService
from app.services.processing_service import ProcessingPaymentService
from app.settings.settings import AppSettings, PostgresSettings, Settings


class ApplicationProvider(Provider):
    """Провайдер зависимостей"""
    settings = from_context(provides=Settings, scope=Scope.APP)
    postgres_config = from_context(provides=PostgresSettings, scope=Scope.APP)
    app_config = from_context(provides=AppSettings, scope=Scope.APP)
    database = provide(Database, scope=Scope.APP)
    unit_of_work = provide(UnitOfWork, scope=Scope.REQUEST, provides=IUnitOfWork)
    payment_service = provide(PaymentService, scope=Scope.REQUEST, provides=IPaymentService)
    outbox_service = provide(OutBoxService, scope=Scope.REQUEST, provides=IOutboxService)
    webhook_adapter = provide(WebhookAdapter, scope=Scope.REQUEST, provides=IWebhookAdapter)
    gateway_adapter = provide(PaymentGatewayAdapter, scope=Scope.REQUEST, provides=IPaymentGatewayAdapter)
    processing_service = provide(ProcessingPaymentService, scope=Scope.REQUEST, provides=IProcessingPaymentService)
    flood_payments_service = provide(FloodPaymentTestService, scope=Scope.REQUEST, provides=IFloodPaymentsTestService)
