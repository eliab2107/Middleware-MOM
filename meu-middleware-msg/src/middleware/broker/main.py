# main.py
from broker.subscription_manager import SubscriptionManager
from broker.notification_engine import NotificationEngine
from broker.notification_consumer import NotificationConsumer
from broker.queue_manager import QueueManager
from network.server_request_handler import ServerRequestHandler
from network.client_request_handler import ClientRequestHandler
from invoker.invoker import Invoker 
from utils.marshaller import Marshaller
import asyncio

async def main():
    marshaller = Marshaller()
    server_request_handler = ServerRequestHandler("localhost", 5001)
    client_request_handler = ClientRequestHandler()
    queue_manager = QueueManager()


    invoker = Invoker(
        marshaller,
        server_request_handler,
        client_request_handler
    )
    subscription_manager = SubscriptionManager()
        
    notification_consumer = NotificationConsumer(subscription_manager, invoker)
    notification_engine = NotificationEngine(queue_manager, notification_consumer, subscription_manager)
    

    invoker.register_service("notification_engine", notification_engine)
    
    srh = ServerRequestHandler(
        host="localhost",
        port=5001,
        callback=invoker.invoke   
    )

    print("Broker iniciado na porta 5001")
    asyncio.create_task(notification_engine.start_consumer())

    await srh.start()
    

if __name__ == "__main__":
    asyncio.run(main())
