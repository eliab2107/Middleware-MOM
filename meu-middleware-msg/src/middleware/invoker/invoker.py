from network.server_request_handler import ServerRequestHandler
from network.client_request_handler import ClientRequestHandler
from utils.marshaller import Marshaller
from utils.protocol import Message
from typing import Any, Dict
import asyncio
class Invoker:
    def __init__(self, marshaller: Marshaller, server_request_handler: ServerRequestHandler, client_request_handler:ClientRequestHandler):
        self.srh = server_request_handler
        self.marshaller = marshaller
        self.crh = client_request_handler
        self.services: Dict[str, Any] = {}

    def register_service(self, service_name: str, service_instance: Any):
        """
        Registra uma instância de serviço. O Invoker só se importa que a instância 
        tenha métodos chamáveis.
        """
        if service_name in self.services:
            raise ValueError(f"Serviço '{service_name}' já está registrado.")
            
        self.services[service_name] = service_instance
       

    async def invoke(self, args) -> Dict[str, Any]:
        """
        Executa o método solicitado pelo payload. 
        """
        connection = args[0]
        envelope = args[1]
        envelope_unmarshaller = self.marshaller.unmarshal(envelope)
        message = Message(envelope_unmarshaller)
        service_name = message.service
        method_name = message.method
        message.args.append(connection) 
        
        if not service_name or not method_name:
            return self.marshaller.marshal({"status": 400, "error": "Payload inválido: 'service' e 'method' são obrigatórios.", "ack": False})
      
        service_instance = self.services.get(service_name)
        
        if service_instance is None:
            return self.marshaller.marshal({"status": 404, "error": f"Serviço '{service_name}' não registrado no Invoker.", "ack": False})

        method_callable = getattr(service_instance, method_name, None)
        if method_callable is None or not callable(method_callable):
            return self.marshaller.marshal({"status": 404, "error": f"Método '{method_name}' não é chamável no serviço '{service_name}'.", "ack": False})
        
      
        try:
            if asyncio.iscoroutinefunction(method_callable):
                await method_callable(message.args)
            else:
                method_callable(message.args)
            response = {"ack": True}
            return self.marshaller.marshal(response)
        
        except TypeError as e:
            # Erro de Argumentos (o payload passou args/kwargs errados)
            return self.marshaller.marshal({"status": 400, "error": f"Argumentos incorretos ou faltantes para o método: {e}", "ack": False})
        except Exception as e:
            # Erro na lógica de negócio do serviço (Divisão por zero, etc.)
            return self.marshaller.marshal({"status": 500, "error": "Erro interno do serviço.", "details": str(e), "ack": False})
        
        
    async def loop(self):
        print("Invoker iniciado, aguardando mensagens...")

        while True:
            try:
                raw_message = self.srh.receive()
                message = self.marshaller.unmarshal(raw_message)
               
                result = self.invoke(message)
                print("Result:", result)
                response = self.marshaller.marshal(result)
                self.srh.send(response)

            except ConnectionError:
                print("Cliente desconectou.")
                break
            
        
    def process_message(self, msg: dict) -> dict:
        operation = msg["method"]
        if operation == "publish":
            topic = msg["topic"]
            payload = msg["payload"]
            self.notification_engine.publish(topic, payload)
            return {"status": "ack"}

        elif operation == "subscribe":
            queue = msg["queue"]
            self.notification_engine.subscribe(queue)
            return {"status": "ack"}

        elif operation == "unsubscribe":
            queue = msg["queue"]
            self.notification_engine.unsubscribe(queue)
            return {"status": "ack"}

        elif operation == "create_queue":
            queue = msg["queue"]
            self.notification_engine.create_queue(queue)
            return {"status": "ack"}

        elif operation == "close_connection":
            self.srh.close()
            return {"status": "ack"}
        
