from middleware.client.proxy import ClientProxy
from typing import Callable 
from middleware.network.server_request_handler import ServerRequestHandler
import asyncio
class Subscriber:
    def __init__(self, client_proxy:ClientProxy, my_host:str, my_port:int, server_host:str, server_port:int, func:Callable, ):
        self.client_proxy = client_proxy
        self.callback = func
        self.my_host = my_host
        self.my_port = my_port
        self.server_host = server_host
        self.server_port = server_port
        self.srh = ServerRequestHandler(my_host, my_port, func)
      
    async def start_server(self):
        await self.srh.start()
        print(f"Subscriber server started at {self.my_host}:{self.my_port}")
            
            
    def subscribe(self, topic:str):
        self.client_proxy.connect(self.server_host, self.server_port)
        self.client_proxy.subscribe(topic)
        print(f"Subscribed to topic: {topic}")
        

    
    