
from invoker.invoker import Invoker
from broker.queue_manager import QueueManager
from broker.subscription_manager import SubscriptionManager

class NotificationConsumer():
    def __init__(self, subscription_manager:SubscriptionManager, invoker: Invoker):
        self.sub_manager = subscription_manager
        self.invoker = invoker
        
    async def notify(self, topic, message):
        subscribers = self.sub_manager.get_subscribers(topic)
        for connection in subscribers:
            await self.invoker.send_to_subscriber(connection, message)
            
