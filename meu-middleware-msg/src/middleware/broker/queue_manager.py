"""Queue manager with TTL support."""
import asyncio
import time
from typing import Dict, List, Optional
from middleware.protocol import Message


class QueueManager:
    def __init__(self):
        # queue_name -> list of Message
        self._queues: Dict[str, List[Message]] = {}
        self._locks: Dict[str, asyncio.Lock] = {}

    def _ensure(self, name: str):
        if name not in self._queues:
            self._queues[name] = []
            self._locks[name] = asyncio.Lock()

    async def enqueue(self, name: str, message: Message) -> None:
        self._ensure(name)
        async with self._locks[name]:
            self._queues[name].append(message)

    async def dequeue(self, name: str) -> Optional[Message]:
        """Return the oldest non-expired message, or None if none available."""
        self._ensure(name)
        async with self._locks[name]:
            q = self._queues[name]
            i = 0
            while i < len(q):
                msg = q[i]
                if msg.is_expired():
                    # discard expired message and continue scanning
                    q.pop(i)
                    continue
                # first non-expired message
                return q.pop(i)
            return None

    async def size(self, name: str) -> int:
        self._ensure(name)
        async with self._locks[name]:
            q = self._queues[name]
            return sum(1 for m in q if not m.is_expired())
