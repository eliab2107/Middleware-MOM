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
    
    async def publish(self, message: Message) -> None:
        await self.storage.enqueue(message.topic, message)
        return {"status": "ack"}
    
    
    async def susbcribe(self, topic: str, endpoint:tuple[str, int]) -> None:
        with self.global_lock:
            self.storage.get_queues()  # Ensure the topic exists
            if topic not in  self.storage.get_queues() :
                self.storage.create_queue(topic)
            await self.sub_manager.add_subscriber(topic, endpoint)
        
    
    async def unsubscribe(self, topic: str, subscriber:tuple[str, int]) -> None:
        self.sub_manager.remove_subscriber(topic, subscriber)
    
    
    async def create_queue(self, queue: str) -> None:
        self.storage.create_queue(queue)
    
    
    def start_consumer(self) -> None:
        if self._consumer_thread and self._consumer_thread.is_alive():
            return

        def _thread_target():
            loop = asyncio.new_event_loop()
            self._consumer_loop = loop
            asyncio.set_event_loop(loop)
            try:
                # schedule consumer.run() and keep loop running
                coro = getattr(self.consumer, "run", None)
                if coro is None:
                    return
                task = loop.create_task(coro())
                loop.run_forever()
                # when stopped, cancel pending tasks
                pending = asyncio.all_tasks(loop)
                for p in pending:
                    p.cancel()
                loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            finally:
                try:
                    loop.close()
                except Exception:
                    pass

        t = threading.Thread(target=_thread_target, daemon=True)
        t.start()
        self._consumer_thread = t

    