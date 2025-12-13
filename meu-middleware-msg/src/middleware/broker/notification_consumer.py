import threading
from invoker.invoker import Invoker
#vai usar o invoker para enviar mensagens aos subscribers 

class NotificationConsumer(threading.Thread):
    def __init__(self, subscription_manager):
        super().__init__(daemon=True)
        self.sub_manager = subscription_manager

    def run(self):
        while True:
            # Aqui você implementaria a lógica para consumir mensagens
            # e enviar notificações aos subscribers usando o invoker.
            pass
