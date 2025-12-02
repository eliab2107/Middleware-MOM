"""Queue manager with TTL support."""
import asyncio
import time
from typing import Dict, List, Optional
from middleware.protocol import Message


class QueueManager:
    def __init__(self):
        """Init manager queues"""
        # queue_name -> list of Message
        #self._queues: Dict[str, List[Message]] = {}
        #self._locks: Dict[str, asyncio.Lock] = {}
        ...

    def _ensure(self, name: str):
        """Create/declare a new exchange or topic"""
        ...

    async def enqueue(self, name: str, message: Message) -> None:
        """Add a new message in the queue"""
        ...

    async def dequeue(self, name: str) -> Optional[Message]:
        """Return the oldest non-expired message, or None if none available."""
        ...

    async def size(self, name: str) -> int:
        ...
