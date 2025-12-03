"""Queue manager with TTL support."""
import asyncio
import time
from typing import Dict, List, Optional
from middleware.protocol import Message


class QueueManager:
    def __init__(self):
        """Init manager queues"""
        # queue_name -> list of Message
        self.queues: Dict[str, List[Message]] = {}
        self.locks: Dict[str, asyncio.Lock] = {}
        self.global_lock = asyncio.Lock()


    async def ensure(self, name: str) -> None:
        """Create/declare a new exchange or topic"""
        if name in self.queues:
            return
        async with self.global_lock:
            if name in self.queues:
                return
            self.queues[name] = []
            self.locks[name] = asyncio.Lock()
        
            
    async def enqueue(self, name: str, message: Message) -> None:
        """Add a new message in the queue"""
        await self.ensure(name)
        async with self.locks[name]:
            self.queues[name].append(message)
    

    async def dequeue(self, name: str) -> Optional[Message]:
        """Return the oldest non-expired message, or None if none available."""
        await self.ensure(name)
        async with self.locks[name]:
            queue = self.queues[name]
            while queue:
                message = queue[0]
                if message.is_expired():
                    queue.pop(0)
                    continue
                return queue.pop(0) #Aqui a gente ta apagando a mensagem da fila antes de receber um ack.
            return None
    