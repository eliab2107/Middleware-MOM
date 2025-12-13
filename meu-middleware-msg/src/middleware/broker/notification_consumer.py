import threading
from invoker.invoker import Invoker
from broker.queue_manager import QueueManager
from broker.subscription_manager import SubscriptionManager
import time

class NotificationConsumer(threading.Thread):
    def __init__(self, subscription_manager:SubscriptionManager, invoker: Invoker):
        super().__init__(daemon=True)
        self.sub_manager = subscription_manager
        self.invoker = invoker
        
    def notify(self, topic):
        subscribers = self.sub_manager.get_subscribers(topic)
        for subscriber in subscribers:
            print("SUBSCRIBER", subscriber)
            self.invoker.crh.connect(subscriber, topic)
            self.invoker.crh.send_notification(topic)
            
            
    async def run(self, queue_manager:QueueManager):
        while True:
            print("CONSUMER RUNNING")
            for topic in queue_manager.get_queues():
                print("CHECKING TOPIC", topic)
                subscribers = self.sub_manager.get_subscribers(topic)
                if not subscribers:
                    continue
                message = queue_manager.dequeue(topic)
                print("DEQUEUED MESSAGE", message)
                if message:
                    for subscriber in subscribers:
                        print("SUBSCRIBER", subscriber)
                        print("NOTIFYING SUBSCRIBER", subscriber)
                        self.invoker.crh.connect(subscriber, topic)
                        self.invoker.crh.send_notification(message)
            time.sleep(10)
