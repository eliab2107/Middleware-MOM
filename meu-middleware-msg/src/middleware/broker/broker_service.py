"""Simple in-process broker service with request routing and reply futures."""
import asyncio
from typing import Callable, Optional
from middleware.protocol import Message
from middleware.broker.queue_manager import QueueManager
from middleware.broker.connection import BrokerConnection
import socket

class BrokerService:
    def __init__(self,  host='0.0.0.0', port=5000):
        self.queue_manager = QueueManager()
        self.host = host
        self.port = port
        self.next_connection_id = 1
        self.connection_id_lock = asyncio.Lock()

    async def get_next_id(self) -> int:
        async with self.connection_id_lock:
            current_id = self.next_connection_id
            
            self.next_connection_id += 1
            
            return current_id
        
        
    async def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen()
        server_socket.setblocking(False) # Configuração pra rodar com asyncio

        loop = asyncio.get_event_loop()
        print(f"Broker ouvindo em {self.host}:{self.port}")

        while True:
            conn, addr = await loop.sock_accept(server_socket)
            conn_id = self.get_next_id()
            connection = BrokerConnection(conn_id, conn, addr, self.queue_manager)
            
            loop.create_task(connection.start_listening())
            
            
    def register_handler(self, queue_name: str, handler: Callable[[Message], asyncio.Future]):
        """Register a coroutine/function to process messages from a queue."""
        ...

    async def send(self, queue_name: str, message: Message) -> None:
        """Enqueue a message and try to deliver it to a registered handler."""
        ...

    async def request_response(self, queue_name: str, message: Message, timeout: Optional[float] = None) -> Message:
        """Send a message and wait for a response identified by correlation_id."""
        ...