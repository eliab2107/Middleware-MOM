"""Invoker: calls service methods based on incoming Message."""
from middleware.protocol import Message
from typing import Any
import asyncio


class Invoker:
    def __init__(self, service: Any):
        self.service = service

    async def handle(self, message: Message) -> Message:
        # call the method from the service
        method_name = message.method
        if not hasattr(self.service, method_name):
            resp = Message(
                type="response",
                payload={"error": f"method {method_name} not found"},
                correlation_id=message.correlation_id,
                reply_to=message.reply_to,
            )
            return resp

        method = getattr(self.service, method_name)
        # support sync or async
        result = method(*message.args, **message.kwargs)
        if asyncio.iscoroutine(result):
            result = await result

        resp = Message(
            type="response",
            payload=result,
            correlation_id=message.correlation_id,
            reply_to=message.reply_to,
        )
        return resp
