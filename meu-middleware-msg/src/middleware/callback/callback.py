from middleware.utils.marshaller import Marshaller
from middleware.network.server_request_handler import ServerRequestHandler
from typing import Callable

class Callback:
    def __init__(self, func:Callable):
        if not callable(func):
            raise TypeError("func deve ser uma callable")
        self.func = func
        self.marshaller = Marshaller()
    
    async def run(self, payload):
        payload_unmashaller = self.marshaller.unmarshal(payload)
        self.func(payload_unmashaller)
        