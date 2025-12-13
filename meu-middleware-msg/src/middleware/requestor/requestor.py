from middleware.network.client_request_handler import ClientRequestHandler
from middleware.utils.marshaller import Marshaller

class Requestor:
    def __init__(self):
        self.marshaller = Marshaller()
  
    def connect(self, host: str, port: int):
        self.crh = ClientRequestHandler(host, port)
        self.crh.connect()
        
    def handler(self, envelope):
        raw = self.marshaller.marshal(envelope)
        response_raw = self.crh.send_receive(raw)

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
    
    
    def subscribe(self, queue):
        envelope = {
            "operation": "subscribe",
            "queue": queue
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