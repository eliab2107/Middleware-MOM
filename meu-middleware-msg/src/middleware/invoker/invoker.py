from network.server_request_handler import ServerRequestHandler
from network.client_request_handler import ClientRequestHandler
from utils.marshaller import Marshaller
from broker.notification_engine import NotificationEngine
class Invoker:
    def __init__(self, marshaller: Marshaller, server_request_handler: ServerRequestHandler, notification_engine: NotificationEngine, client_request_handler:ClientRequestHandler):
        self.srh = server_request_handler
        self.marshaller = marshaller
        self.notification_engine = notification_engine
        self.clientRequestHandler = client_request_handler

    def loop(self):
        print("Invoker iniciado, aguardando mensagens...")

        while True:
            try:
                raw_message = self.srh.receive()
                message = self.marshaller.unmarshal(raw_message)

                # PROCESSAMENTO REAL
                result = self.process_message(message)

                # Envio ACK/NACK
                response = self.marshaller.marshal(result)
                self.srh.send(response)

            except ConnectionError:
                print("Cliente desconectou.")
                break

    def process_message(self, msg: dict) -> dict:
        print("Mensagem recebida:", msg)
        return {"status": "ack"}
        
