# main.py
from broker.subscription_manager import SubscriptionManager
from broker.notification_engine import NotificationEngine
from broker.notification_consumer import NotificationConsumer
from network.server_request_handler import ServerRequestHandler
from network.client_request_handler import ClientRequestHandler
from invoker.invoker import Invoker 
from utils.marshaller import Marshaller
from broker.events import EventStorage

def main():
    marshaller = Marshaller()
    server_request_handler = ServerRequestHandler("localhost", 5001)
    client_request_handler = ClientRequestHandler()
    
    subscription_manager = SubscriptionManager()
        
    notification_consumer = NotificationConsumer(subscription_manager)
    event_storage = EventStorage()
    notification_engine = NotificationEngine(event_storage, notification_consumer, subscription_manager)

    

    invoker = Invoker(
        marshaller,
        server_request_handler,
        notification_engine,
        client_request_handler
    )

    invoker.loop()


#A solução para os modulos nao encontrados foi utilizar python -m e o nome da classe que se quer executar
if __name__ == "__main__":
    main()
