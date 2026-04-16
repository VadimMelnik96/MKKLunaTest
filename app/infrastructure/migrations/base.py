from app.infrastructure.models.base import Base
from app.infrastructure.models.outbox import OutboxMessage
from app.infrastructure.models.payments import Payment

models = [
    Base,
    Payment,
    OutboxMessage
]
