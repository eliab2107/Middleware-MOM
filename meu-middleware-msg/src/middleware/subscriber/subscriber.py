from middleware.client.proxy import ClientProxy
from middleware.callback.callback import Callback
from typing import Callable 
import asyncio
class Subscriber:
    def __init__(self, client_proxy:ClientProxy, my_host:str, my_port:int, server_host:str, server_port:int, func:Callable):
        self.client_proxy = client_proxy
        self.callback = Callback(func, my_host, my_port)
        self.my_host = my_host
        self.my_port = my_port
        self.server_host = server_host
        self.server_port = server_port
        self.task = asyncio.create_task(self.callback.run())
        #self.task.done()
    
    def subscribe(self, topic:str):
        self.client_proxy.connect(self.server_host, self.server_port)
        self.client_proxy.subscribe(topic)
        print(f"Subscribed to topic: {topic}")
        

    
    