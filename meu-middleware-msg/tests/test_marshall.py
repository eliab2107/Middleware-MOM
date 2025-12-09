import unittest
from src.middleware.utils.marshaller import Marshaller # Ajuste o caminho de importação!

class TestMarshaller(unittest.TestCase):
    
    def setUp(self):
        """Prepara o Marshaller para cada teste."""
        self.marshaller = Marshaller()
        
    def test_basic_round_trip(self):
        """Testa a conversão e reconversão de uma mensagem simples."""
        
        original_message = {
            "service": "calculadora",
            "method": "somar",
            "args": [10, 5],
            "correlation_id": "uuid-12345"
        }
        
        # 1. Marshalling (Dict -> Bytes)
        marshaled_bytes = self.marshaller.marshal(original_message)
        
        # 2. Verifica se o resultado é bytes e não está vazio
        self.assertIsInstance(marshaled_bytes, bytes)
        self.assertTrue(len(marshaled_bytes) > 0)
        
        # 3. Unmarshalling (Bytes -> Dict)
        unmarshaled_dict = self.marshaller.unmarshal(marshaled_bytes)
        
        # 4. Verifica se o objeto retornado é idêntico ao original
        self.assertEqual(original_message, unmarshaled_dict)

    def test_unicode_and_types(self):
        """Testa caracteres especiais e tipos de dados complexos (float, bool)."""
        
        unicode_message = {
            "string_unicode": "Mensagem com acentuação: Áéãçü",
            "number_float": 3.14159,
            "boolean": True,
            "lista_mista": [1, None, "teste"]
        }
        
        marshaled = self.marshaller.marshal(unicode_message)
        unmarshaled = self.marshaller.unmarshal(marshaled)
        
        # Garante que os caracteres e os tipos foram preservados
        self.assertEqual(unicode_message, unmarshaled)

    def test_empty_payload(self):
        """Testa o comportamento com dados vazios."""
        
        with self.assertRaises(ValueError) as cm:
            self.marshaller.unmarshal(b'')
            
        self.assertIn("Payload vazio recebido", str(cm.exception))

    def test_invalid_json_bytes(self):
        """Testa se o unmarshaller levanta exceção para dados corrompidos."""
        
        # Bytes inválidos (não é JSON)
        invalid_bytes = b'isto nao e um json valido'
        
        with self.assertRaises(ValueError) as cm:
            self.marshaller.unmarshal(invalid_bytes)
        
        # Opcional: Verifica se a mensagem de erro é a esperada (JSONDecodeError)
        self.assertIn("falha ao desserializar (payload inválido)", str(cm.exception))


if __name__ == '__main__':
    unittest.main()