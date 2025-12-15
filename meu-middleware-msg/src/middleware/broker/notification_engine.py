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
        
    
    async def publish(self, args) -> None:
        topic = args[0]
        message = Message(args[1])
        await self.storage.enqueue(topic, message)    
        
    
    async def subscribe(self, args) -> None:
        topic = args[0]
        connection = args[len(args)-1]
        with self.global_lock:  
            if topic not in  self.storage.get_queues() :
                self.storage.create_queue(topic)
            
            self.sub_manager.add_subscriber(topic, connection)
        
    
    def unsubscribe(self, topic: str, subscriber:tuple[str, int]) -> None:
        self.sub_manager.remove_subscriber(topic, subscriber)
    
    
    def create_queue(self, queue: str) -> None:
        self.storage.create_queue(queue)
    
    
    def consume(self, queue) -> None:
        self.consumer.start_consuming()
    
    
    def start_consumer(self) -> None:
        asyncio.create_task(self.consumer.run(self.storage))

       
    