import random

import structlog

from app.domain.exceptions import WebhookError
from app.infrastructure.adapters.interfaces import IWebhookAdapter

logger = structlog.get_logger(__name__)

class WebhookAdapter(IWebhookAdapter):
    """Имитация адаптера webhook"""

    async def send(self, url: str, payload: dict) -> bool:
        """Метод отправки информации на вебхук"""
        logger.info(f"Отправляем {payload} на {url}")
        if random.random() < 0.1:
            raise WebhookError
        else:
            return True
