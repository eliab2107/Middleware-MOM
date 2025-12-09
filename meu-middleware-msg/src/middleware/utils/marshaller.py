from typing import Any, Dict
import json
from json.decoder import JSONDecodeError

class Marshaller:
    """Implementa a serialização JSON para o payload do middleware."""

    def marshal(self, message: Dict[str, Any]) -> bytes:
        """Converte um dict para bytes (payload de rede)."""
        try:
            json_string = json.dumps(message, separators=(",", ":"), ensure_ascii=False)
            return json_string.encode("utf-8")
        except TypeError as e:
            raise ValueError(f"falha ao serializar (objeto não JSON-compatível): {e}") from e
        except Exception as e:
            raise ValueError(f"falha desconhecida ao serializar: {e}") from e


    def unmarshal(self, data: bytes) -> Dict[str, Any]:
        """Converte bytes (JSON UTF-8) de volta para um dict."""
        
        if not data:
            raise ValueError("falha ao desserializar: Payload vazio recebido. Conexão encerrada ou dados perdidos.")
            
        try:
            s = data.decode("utf-8") 
            return json.loads(s)
            
        except UnicodeDecodeError as e:
            raise ValueError(f"falha ao decodificar (não é UTF-8 válido): {e}") from e
        except JSONDecodeError as e:
            raise ValueError(f"falha ao desserializar (payload inválido): {e}") from e
        except Exception as e:
            raise ValueError(f"falha desconhecida ao desserializar: {e}") from e