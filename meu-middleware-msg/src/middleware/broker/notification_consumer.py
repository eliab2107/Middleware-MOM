import threading
from invoker.invoker import Invoker
#vai usar o invoker para enviar mensagens aos subscribers 

class NotificationConsumer(threading.Thread):
    def __init__(self, subscription_manager):
        super().__init__(daemon=True)
        self.sub_manager = subscription_manager

    def run(self):
        while True:
            event = self.engine.queue.get()
            topic = event["topic"]
            subscribers = self.sub_manager.get_subscribers(topic)

            for s in subscribers:
                self.invoker.send_notification(s.endpoint, event["data"])
