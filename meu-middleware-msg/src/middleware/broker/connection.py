"""Connection abstraction used by clients and servers to interact with the broker."""
from middleware.protocol import Message
from typing import Optional
from socket import socket
import asyncio
from middleware.broker.queue_manager import QueueManager

class BrokerConnection:
    def __init__(self, id:int, conn: socket, addr:tuple[str, int], queue_manager:QueueManager):
        self.id = id
        self.conn = conn
        self.addr = addr
        self.queue_manager = queue_manager
        

    async def send(self, queue: str, message: Message) -> None:
        ...

    async def request(self, queue: str, message: Message, timeout: Optional[float] = None) -> Message:
        ...
    
    def close(self):
        ...