from typing import Any, Dict, Callable

class Invoker:
    """
    Recebe um payload de requisição e executa o método correspondente 
    no serviço registrado.
    """
    
    def __init__(self):
        """Inicializa o registro de serviços vazios."""
        self.services: Dict[str, Any] = {}

    def register_service(self, service_name: str, service_instance: Any):
        """
        Adiciona uma instância de serviço ao registro.
        Ex: invoker.register_service('calculadora', Calculadora())
        """
        if service_name in self.services:
            raise ValueError(f"Serviço '{service_name}' já está registrado.")
            
        self.services[service_name] = service_instance


    def invoke(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa o método solicitado pelo payload e retorna o resultado.
        """
        service_name = payload.get("service")
        method_name = payload.get("method")
        args = payload.get("args", [])
        kwargs = payload.get("kwargs", {})
        
        service_instance = self.services.get(service_name)
        
        if not service_instance:
            return {"status": 404, "error": f"Serviço '{service_name}' não registrado."}

        if not hasattr(service_instance, method_name):
            return {"status": 404, "error": f"Método '{method_name}' não encontrado no serviço '{service_name}'."}

        method_callable: Callable = getattr(service_instance, method_name)
        
        try:
            result = method_callable(*args, **kwargs)
            
            return {
                "status": 200, 
                "result": result,
                "correlation_id": payload.get("correlation_id") 
            }
        except TypeError:
            return {"status": 400, "error": "Argumentos incorretos para o método."}
        except Exception as e:
            return {"status": 500, "error": "Erro interno do serviço.", "details": str(e)}