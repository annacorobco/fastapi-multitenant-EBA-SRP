import redis.asyncio as redis

from app.config import settings
from app.services.cache.base import CacheService
from app.logger import logger


class RedisCacheService(CacheService):
    def __init__(self):
        self.client = None

    async def connect(self):
        self.client = redis.from_url(settings.REDIS_URL, decode_responses=True)

    async def get(self, key: str) -> str | None:
        try:
            return await self.client.get(key)
        except Exception as e:
            logger.info(f"[Redis Error] Failed to get key: {e}")
            return None

    async def set(self, key: str, value: str, expire: int = 3600) -> None:
        await self.client.set(key, value, ex=expire)

    async def delete(self, key: str) -> None:
        await self.client.delete(key)

    async def close(self):
        if self.client:
            await self.client.close()
