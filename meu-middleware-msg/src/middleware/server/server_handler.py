"""Server Handler that registers an invoker with the broker."""
from middleware.broker.broker_service import BrokerService
from middleware.server.invoker import Invoker
from middleware.protocol import Message
from typing import Any


class ServerHandler:
    def __init__(self, broker: BrokerService, queue: str = "requests"):
        self.broker = broker
        self.queue = queue
        self.invoker: Invoker = None

    def register_service(self, service: Any):
        ...

    async def _handle(self, message: Message) -> Message:
        ...
