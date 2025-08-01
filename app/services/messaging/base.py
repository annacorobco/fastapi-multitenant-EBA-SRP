from abc import ABC, abstractmethod


class MessageBrokerService(ABC):
    @abstractmethod
    async def publish(self, queue: str, message: str) -> None: pass
