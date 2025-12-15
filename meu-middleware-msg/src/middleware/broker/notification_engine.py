from utils.protocol import Message
from broker.queue_manager import QueueManager
from broker.subscription_manager import SubscriptionManager
from broker.notification_consumer import NotificationConsumer
import asyncio
import time
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
        print("AAAAAAAAAAARGS: ", args)
        topic = args[0]
        connection = args[len(args)-1] 

        if topic not in self.storage.get_queues() :
            print()
            await self.storage.ensure(topic)
        await self.sub_manager.add_subscriber(topic, connection)
    
    
    def unsubscribe(self, topic: str, subscriber:tuple[str, int]) -> None:
        self.sub_manager.remove_subscriber(topic, subscriber)
    
    
    async def start_consumer(self) -> None:
        while True:
            queues = list(self.storage.queues.keys())
            print("filas: ", self.storage.queues)
            print("subs: ",  self.sub_manager.subscribers)
            for queue in queues:
                if len(self.sub_manager.get_subscribers(queue)) > 0:
                    message = await self.storage.dequeue(queue)

                    if message is not None:
                        await self.consumer.notify(queue, message)

            await asyncio.sleep(3) 
                

       
    