from typing import Callable
import asyncio
from middleware.client.proxy import ClientProxy
from middleware.network.client_request_handler import ClientRequestHandler
from middleware.network.server_request_handler import ServerRequestHandler
from middleware.callback.callback import Callback

class Subscriber:
    """
    Subscriber
    - SRH: recebe eventos do broker
    - CRH (ClientProxy): envia SUBSCRIBE / UNSUBSCRIBE
    """

    def __init__(self, broker_host, broker_port, my_host: str,  my_port: int, callback: Callable[[bytes], None] ):
        self.client_proxy = ClientProxy(broker_host, broker_port)
        self.callback = Callback(callback)
        self.my_host = my_host
        self.my_port = my_port
        self.srh = ServerRequestHandler(my_host, my_port, self.callback.run)

    
    async def start_listen(self):
        print(f"[SUBSCRIBER] SRH escutando em {self.my_host}:{self.my_port}")
        await self.srh.start(self.srh.handle_connection)


    async def subscribe(self, topic: str):
        await self.client_proxy.connect()
        response = await self.client_proxy.subscribe(topic, self.my_host, self.my_port)

        print(f"[SUBSCRIBER] Subscribed to topic '{topic}': {response}")


    async def start(self,):
       self.server_task = asyncio.create_task(self.start_listen())
       await self.server_task
    
