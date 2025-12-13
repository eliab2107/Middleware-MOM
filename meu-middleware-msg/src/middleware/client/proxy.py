from middleware.requestor.requestor import Requestor
from middleware.callback.callback import Callback
from middleware.protocol import Message
class ClientProxy:
    def __init__(self):
        self.requestor = Requestor()
    
    
    def set_callback(self, func):
        """Define a função de callback para mensagens recebidas."""
        self.callback = Callback(func)
        
        
    def connect(self, host: str, port: int):
        """Estabelece conexão com o broker."""
        self.requestor.connect(host, port)
        

    def publish(self, topic: str,  payload: str = "hello world", reply_to: str = "",ttl_ms: int = 0, type:str="send", args: list=[], kwargs:dict={}):
        if not topic:
            raise ValueError("Precisa informar um tópico para poder publicar.")
        message = {"topic": topic, "payload": payload, "reply_to": reply_to, "ttl_ms": ttl_ms, "type": type, "args": args}
        resp = self.requestor.publish(topic, message)
        print(f"Publish response: {resp}")

    def subscribe(self, queue: str):
        return self.requestor.subscribe(queue)

    def unsubscribe(self, queue: str):
        return self.requestor.unsubscribe(queue)


    def create_queue(self, queue: str):
        return self.requestor.create_queue(queue)


    def consume(self, queue: str):
        return self.requestor.consume(queue)


    def close(self):
        return self.requestor.close_connection()
