import struct
import socket
#O server request handler precisa aceitar as conexoes, receber suas mensagens e envia-las para o invoker que saberá o que fazer com elas.
from typing import Callable, Awaitable, Dict, Any
import asyncio
class ServerRequestHandler:
    """
    Mantém uma conexão persistente.
    NÃO tem loop próprio.
    Lê e escreve mensagens quando a classe superior pedir.
    """
    def __init__(self, host: str, port: int, callback: Callable[[Dict[str, Any]], Awaitable[None]] = None):
        self.host = host
        self.port = port
        self.callback = callback
        #self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock.bind((self.host, self.port))
        #self.sock.listen()  # Escuta por conexões
    
    async def start(self):
        server = await asyncio.start_server(
            self.handle,
            self.host,
            self.port
        )
        async with server:
            await server.serve_forever()
            
    
    async def handle(self, reader, writer):
        connection = (reader, writer)

        try:
            while True:
                payload = await self.receive(reader)

                request = [connection, payload]

                response = await self.callback(request)
                if response:
                    await self.send(response, connection[1])

 
        except (asyncio.IncompleteReadError, ConnectionResetError):
            pass
        finally:
            writer.close()
            await writer.wait_closed()
            
            
    async def receive(self, reader) -> bytes:
        """Recebe uma mensagem do socket (bloqueante)."""
        print(f"Aguardando conexão de cliente no endereço {self.host}:{self.port}...")
        size_raw = await reader.readexactly(4)
        size = struct.unpack("!I", size_raw)[0]
        payload = await reader.readexactly(size)
        return payload


    async def send(self, payload: bytes, writer:asyncio.StreamWriter):
        """Envia mensagem usando o mesmo socket persistente."""
        size = struct.pack("!I", len(payload))
        writer.write(size + payload)
        await writer.drain()

    def recv_exact(self, n):
        data = b""
        while len(data) < n:
            chunk = self.conn.recv(n - len(data))
            if not chunk:
                raise ConnectionError("Conexão encerrada")
            data += chunk
        return data
