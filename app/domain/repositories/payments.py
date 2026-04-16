from app.common.repositories.repository import SQLAlchemyRepository
from app.domain.repositories.interfaces import IPaymentsRepo
from app.domain.schemas.payments import PaymentDTO
from app.infrastructure.models.payments import Payment


class PaymentsRepo(SQLAlchemyRepository, IPaymentsRepo):
    """Репо платежей"""
    model = Payment
    response_dto = PaymentDTO
