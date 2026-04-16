import aio_pika
from faststream.rabbit import ExchangeType, RabbitBroker, RabbitExchange, RabbitQueue

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
    """Объявление и связывание через нативный aio_pika"""
    q_main: aio_pika.RobustQueue = await broker.declare_queue(payments_queue)
    ex_main: aio_pika.RobustExchange = await broker.declare_exchange(payments_exchange)
    await q_main.bind(ex_main, routing_key="payments.new")

    q_retry1: aio_pika.RobustQueue = await broker.declare_queue(retry_queue_1)
    ex_retry1: aio_pika.RobustExchange = await broker.declare_exchange(retry_exchange_1)
    await q_retry1.bind(ex_retry1, routing_key="payments.retry.1")

    q_retry2: aio_pika.RobustQueue = await broker.declare_queue(retry_queue_2)
    ex_retry2: aio_pika.RobustExchange = await broker.declare_exchange(retry_exchange_2)
    await q_retry2.bind(ex_retry2, routing_key="payments.retry.2")

    q_dead: aio_pika.RobustQueue = await broker.declare_queue(dlq_queue)
    ex_dead: aio_pika.RobustExchange = await broker.declare_exchange(dlx_exchange)
    await q_dead.bind(ex_dead, routing_key="payments.dead")
