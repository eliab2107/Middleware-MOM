"""Simple in-process broker service with request routing and reply futures."""
import asyncio
from typing import Callable, Dict, Optional
from middleware.protocol import Message
from middleware.broker.queue_manager import QueueManager


class BrokerService:
    def __init__(self):
        self.queue_manager = QueueManager()
        ...

    def register_handler(self, queue_name: str, handler: Callable[[Message], asyncio.Future]):
        """Register a coroutine/function to process messages from a queue."""
        ...

    async def send(self, queue_name: str, message: Message) -> None:
        """Enqueue a message and try to deliver it to a registered handler."""
        ...

    async def request_response(self, queue_name: str, message: Message, timeout: Optional[float] = None) -> Message:
        """Send a message and wait for a response identified by correlation_id."""
        ...
