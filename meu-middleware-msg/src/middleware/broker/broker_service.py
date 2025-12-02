"""Simple in-process broker service with request routing and reply futures."""
import asyncio
from typing import Callable, Dict, Optional
from middleware.protocol import Message
from middleware.broker.queue_manager import QueueManager


class BrokerService:
    def __init__(self):
        self.qm = QueueManager()
        self.handlers: Dict[str, Callable[[Message], asyncio.Future]] = {}
        self._pending_replies: Dict[str, asyncio.Future] = {}

    def register_handler(self, queue_name: str, handler: Callable[[Message], asyncio.Future]):
        """Register a coroutine/function to process messages from a queue."""
        self.handlers[queue_name] = handler

    async def send(self, queue_name: str, message: Message) -> None:
        """Enqueue a message and try to deliver it to a registered handler."""
        await self.qm.enqueue(queue_name, message)
        await self._try_deliver(queue_name)

    async def _try_deliver(self, queue_name: str):
        handler = self.handlers.get(queue_name)
        if not handler:
            return
        while True:
            msg = await self.qm.dequeue(queue_name)
            if msg is None:
                break
            if msg.is_expired():
                # already expired; skip
                continue
            try:
                result = handler(msg)
                if asyncio.iscoroutine(result):
                    result = await result
                # if handler returned a Message (response), route it
                if isinstance(result, Message) and result.reply_to:
                    corr = result.correlation_id
                    fut = self._pending_replies.pop(corr, None)
                    if fut and not fut.done():
                        fut.set_result(result)
            except Exception as e:
                corr = getattr(msg, "correlation_id", None)
                if corr:
                    fut = self._pending_replies.pop(corr, None)
                    if fut and not fut.done():
                        fut.set_exception(e)

    async def request_response(self, queue_name: str, message: Message, timeout: Optional[float] = None) -> Message:
        """Send a message and wait for a response identified by correlation_id."""
        if not message.correlation_id:
            raise ValueError("message must have correlation_id for request_response")
        loop = asyncio.get_running_loop()
        fut: asyncio.Future = loop.create_future()
        self._pending_replies[message.correlation_id] = fut
        await self.send(queue_name, message)
        try:
            return await asyncio.wait_for(fut, timeout)
        finally:
            self._pending_replies.pop(message.correlation_id, None)
