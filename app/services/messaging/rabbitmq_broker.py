import aio_pika

from app.config import settings
from app.services.messaging.base import MessageBrokerService

from app.logger import logger


class RabbitMQBroker(MessageBrokerService):
    def __init__(self):
        self.url = settings.RABBITMQ_URL
        self.connection = None
        self.channel = None

    async def connect(self):
        if self.connection is None:
            self.connection = await aio_pika.connect_robust(self.url)
            self.channel = await self.connection.channel()

    async def publish(self, queue: str, message: str) -> None:
        if not self.channel:
            logger.exception("[RabbitMQ Error] Channel not initialized.")
            return
        await self.connect()
        try:
            await self.channel.default_exchange.publish(
                aio_pika.Message(body=message.encode()),
                routing_key=queue
            )
        except Exception as e:
            logger.exception(f"[RabbitMQ Error] Publish failed: {e}")
