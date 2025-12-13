import asyncio
class SubscriptionManager:
    #Cada subscriber representa o endpoint para onde as notificacoes serao enviadas
    def __init__(self):
        self.subscribers = {}  # topic -> list[Subscriber]
        self.lock = asyncio.Lock()
        
    def add_subscriber(self, topic, subscriber):
        with self.lock:
            self.subscribers[topic].append(subscriber)

    def remove_subscriber(self, topic, subscriber_id):
        with self.lock:
            if topic in self.subscribers:
                self.subscribers[topic] = [
                    s for s in self.subscribers[topic] if s.id != subscriber_id
                ]

    def get_subscribers(self, topic):
        with self.lock:
            subscribers = self.subscribers.get(topic, [])
            return subscribers
