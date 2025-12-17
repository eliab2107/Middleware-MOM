from middleware.requestor.requestor import Requestor
from middleware.callback.callback import Callback
from middleware.protocol import Message
import asyncio
class ClientProxy:
    def __init__(self, server_host:str, server_port:int, callback:Callback = None):
        self.requestor = Requestor(server_host, server_port, callback)
        self.server_host = server_host
        self.server_port = server_port
        self.callback = callback
        
    async def connect(self):
        """Estabelece conexão com o broker."""
        await self.requestor.connect()
  
    
    async def publish(self, topic: str,  payload: str = "hello world", reply_to: str = "",ttl_ms: int = 0, type:str="send", args: list=[], kwargs:dict={}):
        if not topic:
            raise ValueError("Precisa informar um tópico para poder publicar.")
        message = {"topic": topic, "payload": payload, "reply_to": reply_to, "ttl_ms": ttl_ms, "type": type, "args": args}
        resp = await self.requestor.publish(topic, message)
        #print(f"Publish response: {resp}")

    def subscribe(self, queue: str, my_host, my_port):
        return self.requestor.subscribe(queue, my_host, my_port)

    def unsubscribe(self, queue: str):
        return self.requestor.unsubscribe(queue)


    def create_queue(self, queue: str):
        return self.requestor.create_queue(queue)


    def consume(self, queue: str):
        return self.requestor.consume(queue)


    def close(self):
        return self.requestor.close_connection()
