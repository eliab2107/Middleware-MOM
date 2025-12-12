class SubscriptionManager:
    def __init__(self):
        self.subscribers = {}  # topic -> list[Subscriber]

    def add_subscriber(self, topic, subscriber):
        self.subscribers.setdefault(topic, []).append(subscriber)

    def remove_subscriber(self, topic, subscriber_id):
        if topic in self.subscribers:
            self.subscribers[topic] = [
                s for s in self.subscribers[topic] if s.id != subscriber_id
            ]

    def get_subscribers(self, topic):
        return self.subscribers.get(topic, [])
