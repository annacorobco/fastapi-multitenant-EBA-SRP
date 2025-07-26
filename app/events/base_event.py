import asyncio
from typing import Callable, Dict, List, Type


class Event:
    pass


class EventDispatcher:
    _subscribers: Dict[Type[Event], List[Callable]] = {}

    @classmethod
    def subscribe(cls, event_type: Type[Event], handler: Callable):
        cls._subscribers.setdefault(event_type, []).append(handler)

    @classmethod
    async def publish(cls, event: Event):
        handlers = cls._subscribers.get(type(event), [])
        for handler in handlers:
            if asyncio.iscoroutinefunction(handler):
                await handler(event)
            else:
                handler(event)
