"""Client Proxy: exposes remote methods as local coroutines."""
from middleware.broker.connection import BrokerConnection
from middleware.protocol import Message
import uuid
from typing import Any


class Proxy:
    def __init__(self, connection: BrokerConnection, queue: str = "requests", default_ttl_ms: int = 5000):
        self.conn = connection
        self.queue = queue
        self.default_ttl_ms = default_ttl_ms

    async def call(self, method: str, *args, ttl_ms: int = None, **kwargs) -> Any:
        ttl = self.default_ttl_ms if ttl_ms is None else ttl_ms
        corr = str(uuid.uuid4())
        msg = Message(
            type="request",
            method=method,
            args=list(args),
            kwargs=kwargs,
            reply_to="client",
            correlation_id=corr,
            ttl_ms=ttl,
        )
        resp = await self.conn.request(self.queue, msg, timeout=(ttl / 1000.0) + 1.0)
        # assume payload in response
        return resp.payload
