"""Client Proxy: exposes remote methods as local coroutines."""
from middleware.broker.connection import BrokerConnection
from middleware.protocol import Message
import uuid
from typing import Any


class Proxy:
    def __init__(self, connection: BrokerConnection, queue: str = "requests", default_ttl_ms: int = 5000):
        """Class to translate client calls to middleware calls"""

    async def call(self, method: str, *args, ttl_ms: int = None, **kwargs) -> Any:
        """Create the messages and call middleware"""