from app.services.cache.redis_cache import RedisCacheService
from app.services.messaging.rabbitmq_broker import RabbitMQBroker


redis_cache = RedisCacheService()
rabbitmq_broker = RabbitMQBroker()
