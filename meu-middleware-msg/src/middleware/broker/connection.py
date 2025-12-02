"""Connection abstraction used by clients and servers to interact with the broker."""
from middleware.broker.broker_service import BrokerService
from middleware.protocol import Message
from typing import Optional
import asyncio


class BrokerConnection:
    def __init__(self, broker: BrokerService):
        ...

    async def send(self, queue: str, message: Message) -> None:
        ...

    async def request(self, queue: str, message: Message, timeout: Optional[float] = None) -> Message:
        ...
