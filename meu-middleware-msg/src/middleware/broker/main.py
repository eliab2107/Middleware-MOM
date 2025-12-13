# main.py
from broker.subscription_manager import SubscriptionManager
from broker.notification_engine import NotificationEngine
from broker.notification_consumer import NotificationConsumer
from broker.queue_manager import QueueManager
from network.server_request_handler import ServerRequestHandler
from network.client_request_handler import ClientRequestHandler
from invoker.invoker import Invoker 
from utils.marshaller import Marshaller

def main():
    marshaller = Marshaller()
    server_request_handler = ServerRequestHandler("localhost", 5001)
    client_request_handler = ClientRequestHandler()
    queue_manager = QueueManager()
    subscription_manager = SubscriptionManager()
        
    notification_consumer = NotificationConsumer(subscription_manager)
    notification_engine = NotificationEngine(queue_manager, notification_consumer, subscription_manager)

    

    invoker = Invoker(
        marshaller,
        server_request_handler,
        client_request_handler
    )
    
    invoker.register_service("notification_engine", notification_engine)
    invoker.loop()


#A solução para os modulos nao encontrados foi utilizar python -m e o nome da classe que se quer executar
if __name__ == "__main__":
    main()
