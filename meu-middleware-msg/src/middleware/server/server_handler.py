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
        self.invoker = Invoker(service)
        # register the invoker's handle coroutine as the queue handler
        self.broker.register_handler(self.queue, self._handle)

    async def _handle(self, message: Message) -> Message:
        if not self.invoker:
            # no service
            return Message(type="response", payload={"error": "no service registered"}, correlation_id=message.correlation_id, reply_to=message.reply_to)
        return await self.invoker.handle(message)
