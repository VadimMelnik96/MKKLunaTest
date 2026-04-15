from faststream.rabbit import RabbitBroker, RabbitExchange, RabbitQueue, ExchangeType


payments_exchange = RabbitExchange(
    "payments",
    type=ExchangeType.DIRECT,
    durable=True,
)


dlx_exchange = RabbitExchange(
    "payments.dlx",
    type=ExchangeType.DIRECT,
    durable=True,
)


retry_exchange_1 = RabbitExchange(
    "payments.retry.1",
    type=ExchangeType.DIRECT,
    durable=True,
)
retry_exchange_2 = RabbitExchange(
    "payments.retry.2",
    type=ExchangeType.DIRECT,
    durable=True,
)


payments_queue = RabbitQueue(
    "payments.new",
    durable=True,
    arguments={
        "x-dead-letter-exchange": "payments.dlx",
        "x-dead-letter-routing-key": "payments.dead",
    },
)


retry_queue_1 = RabbitQueue(
    "payments.retry.1",
    durable=True,
    arguments={
        "x-message-ttl": 5_000,
        "x-dead-letter-exchange": "payments",
        "x-dead-letter-routing-key": "payments.new",
    },
)


retry_queue_2 = RabbitQueue(
    "payments.retry.2",
    durable=True,
    arguments={
        "x-message-ttl": 15_000,
        "x-dead-letter-exchange": "payments",
        "x-dead-letter-routing-key": "payments.new",
    },
)


dlq_queue = RabbitQueue(
    "payments.dead",
    durable=True,
)


async def declare_queues(broker: RabbitBroker) -> None:
    """Объявление очередей"""
    await broker.declare_exchange(payments_exchange)
    await broker.declare_exchange(dlx_exchange)
    await broker.declare_exchange(retry_exchange_1)
    await broker.declare_exchange(retry_exchange_2)

    await broker.declare_queue(payments_queue)
    await broker.declare_queue(retry_queue_1)
    await broker.declare_queue(retry_queue_2)
    await broker.declare_queue(dlq_queue)