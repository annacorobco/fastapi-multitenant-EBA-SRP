from abc import ABC, abstractmethod


class CacheService(ABC):
    @abstractmethod
    async def get(self, key: str) -> str | None: pass

    @abstractmethod
    async def set(self, key: str, value: str, expire: int = 3600) -> None: pass

    @abstractmethod
    async def delete(self, key: str) -> None: pass
