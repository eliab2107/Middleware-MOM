import asyncio
import socket
import struct
from typing import Tuple
from typing import Callable
class ClientRequestHandler:
    """
    Client Request Handler
    - Abre conexão com o broker
    - Envia mensagens
    - Espera ACK quando necessário
    """

    def __init__(self, host: str = "localhost", port: int=5001, func:Callable = None):
        self.host = host
        self.port = port
        self.reader: asyncio.StreamReader | None = None
        self.writer: asyncio.StreamWriter | None = None
        self.callback = func
       

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection( self.host,  self.port )
    
    
    async def send(self, payload: bytes):
        if not self.writer:
            raise RuntimeError("Conexão não aberta")

        size = struct.pack("!I", len(payload))
        self.writer.write(size + payload)
        await self.writer.drain()


    async def send_and_wait_ack(self, payload: bytes) -> bytes:
        if not self.reader or not self.writer:
            raise RuntimeError("Conexão não aberta")
        
        await self.send(payload)

        size_raw = await self.reader.readexactly(4)
        size = struct.unpack("!I", size_raw)[0]
        return await self.reader.readexactly(size)


    async def close(self):
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()


    async def send_to_subscriber(self,address: Tuple[str, int], payload: bytes) -> None:
        host, port = address

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))

            size = struct.pack("!I", len(payload))
            sock.sendall(size + payload)
        
        
    async def listen(self):
        try:
            while True:
                size_raw = await self.reader.readexactly(4)
                size = struct.unpack("!I", size_raw)[0]
                payload = await self.reader.readexactly(size)

                if self.callback:
                    await self.callback(payload)

        except (asyncio.IncompleteReadError, ConnectionResetError):
            print("Conexão encerrada pelo broker")