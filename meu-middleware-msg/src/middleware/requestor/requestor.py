from middleware.network.client_request_handler import ClientRequestHandler
from middleware.utils.marshaller import Marshaller

class Requestor:
    def __init__(self, server_host, server_port, callback):
        self.marshaller = Marshaller()
        self.crh = ClientRequestHandler(server_host, server_port, callback)
        
        
    async def connect(self):
        await self.crh.connect()
        
    
    async def handler(self, envelope):
        raw = self.marshaller.marshal(envelope)
        response_raw = await self.crh.send_and_wait_ack(raw)
        return self.marshaller.unmarshal(response_raw)
        
    def publish(self, topic, message):
        envelope = {
            "service": "notification_engine",
            "method": "publish",
            "topic": topic,
            "payload":"Hello subscriber",
            "reply_to":"",
            "ttl_ms":0,
            "type":"send",
            "args":[topic, message]
        }

        return self.handler(envelope)
    
    
    def subscribe(self, queue, my_host, my_port):
        envelope = {
            "service": "notification_engine",
            "method": "subscribe",
            "topic": queue,
            "args": [queue, my_host, my_port]
        }

        return self.handler(envelope)
    
    
    def unsubscribe(self, queue):
        envelope = {
            "operation": "unsubscribe",
            "queue": queue
        }

        return self.handler(envelope)
    
    
    def create_queue(self, queue):
        envelope = {
            "operation": "create_queue",
            "queue": queue
        }

        return self.handler(envelope)
    
    
    def close_connection(self):
        envelope = {
            "operation": "close_connection",
        }
        
        return self.handler(envelope)
    
    
    def consume(self, queue):
        envelope = {
            "operation": "consume",
            "queue": queue
        }
        return self.handler(envelope)