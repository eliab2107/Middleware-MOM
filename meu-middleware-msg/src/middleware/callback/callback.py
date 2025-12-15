from middleware.utils.marshaller import Marshaller
from middleware.network.server_request_handler import ServerRequestHandler
from typing import Callable

class Callback:
    def __init__(self, func:Callable, my_host:str="localhost", my_port:int=8000):
        if not callable(func):
            raise TypeError("func deve ser uma callable")
        self.func = func
        self.marshaller = Marshaller()
        self.srh = ServerRequestHandler(my_host, my_port, func)
    
    async def run(self):
        print("Callback iniciado, aguardando mensagens...")

        while True:
            try:
                raw_message = self.srh.receive()
                if not raw_message:
                    continue

                try:
                    message = self.marshaller.unmarshal(raw_message)
                except Exception as e:
                    try:
                        self.srh.send(self.marshaller.marshal({"error": "invalid_payload", "detail": str(e)}))
                    except Exception:
                        pass
                    continue

                
                try:
                    result = self.func(message)
                except Exception as e:
                    result = {"error": "handler_error", "detail": str(e)}

                try:
                    response = self.marshaller.marshal(result)
                    self.srh.send(response)
                except Exception:
                    raise Exception("Erro ao enviar resposta do callback")
            except ConnectionError:
                raise ConnectionError("Conexão encerrada pelo cliente")
            except Exception:
                raise  Exception("Erro desconhecido no callback")
    