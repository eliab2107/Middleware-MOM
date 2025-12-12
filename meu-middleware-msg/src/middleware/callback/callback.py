from middleware.utils.marshaller import Marshaller
from middleware.network.server_request_handler import ServerRequestHandler

class Callback:
    def __init__(self, func):
        self.func = func
        self.marshaller = Marshaller()
        self.srh = ServerRequestHandler('localhost', 8000)
    
    def execute(self):
        print("Callback iniciado, aguardando mensagens...")

        while True:
            try:
                raw_message = self.srh.receive()
                message = self.marshaller.unmarshal(raw_message)

                print("Mensagem recebida no Callback:", message)

                # Executa a função de callback
                result = self.func(message)

                # Envio ACK/NACK
                response = self.marshaller.marshal(result)
                self.srh.send(response)

            except ConnectionError:
                print("Cliente desconectou.")
                break