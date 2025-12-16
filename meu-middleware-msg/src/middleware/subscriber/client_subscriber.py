import asyncio
import struct 
from middleware.client.proxy import ClientProxy
class SubscriberClient:
    def __init__(self, host, port, on_event):
        self.host = host
        self.port = port
        self.on_event = on_event

    async def start(self, queue):
        self.reader, self.writer = await asyncio.open_connection(
            self.host, self.port
        )

        await self.subscribe(self.writer, queue)

        asyncio.create_task(self.listen(self.reader))

    async def subscribe(self, writer, queue):
        payload = b"SUBSCRIBE:news"
        size = struct.pack("!I", len(payload))
        writer.write(size + payload)
        await writer.drain()

    async def listen(self, reader):
        while True:
            size_raw = await reader.readexactly(4)
            size = struct.unpack("!I", size_raw)[0]
            payload = await reader.readexactly(size)

            await self.on_event(payload)