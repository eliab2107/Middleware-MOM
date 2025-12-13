from utils.protocol import Message
from broker.queue_manager import QueueManager
from broker.subscription_manager import SubscriptionManager
from broker.notification_consumer import NotificationConsumer
import asyncio
class NotificationEngine:
    def __init__(self, storage:QueueManager, consumer: NotificationConsumer, sub_manager:SubscriptionManager):
        self.storage = storage
        self.consumer = consumer
        self.sub_manager = sub_manager
        self.global_lock = asyncio.Lock()
        
    
    def publish(self, args) -> None:
        topic = args[0]
        message = Message(args[1])
        print("PUBLISHING MESSAGE", message)
        print("QUEUES: ", self.storage.get_queues())
        print("SUBSCRIBERS: ", self.sub_manager.subscribers )
        self.storage.enqueue(topic, message)
       
    
    
    def subscribe(self, topic: str, endpoint):
        print("SUBSCRIBING TO TOPIC", topic, "AT ENDPOINT", endpoint)
        with self.global_lock:
            self.storage.get_queues()  
            if topic not in  self.storage.get_queues() :
                self.storage.create_queue(topic)
                self.sub_manager.add_subscriber(topic, endpoint)
        
    
    async def unsubscribe(self, topic: str, subscriber:tuple[str, int]) -> None:
        self.sub_manager.remove_subscriber(topic, subscriber)
    
    
    async def create_queue(self, queue: str) -> None:
        self.storage.create_queue(queue)
    
    
    async def consume(self, queue) -> None:
        await self.consumer.start_consuming()
    
    
    async def start_consumer(self) -> None:
        asyncio.create_task(self.consumer.run(self.storage))

       
    