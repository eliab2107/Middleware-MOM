import struct
import socket
#O server request handler precisa aceitar as conexoes, receber suas mensagens e envia-las para o invoker que saberá o que fazer com elas.
class ServerRequestHandler:
    """
    Mantém uma conexão persistente.
    NÃO tem loop próprio.
    Lê e escreve mensagens quando a classe superior pedir.
    """
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()  # Escuta por conexões

    def receive(self) -> bytes:
        """Recebe uma mensagem do socket (bloqueante)."""
        print(f"Aguardando conexão de cliente no endereço {self.host}:{self.port}...")
        self.conn, self.addr = self.sock.accept()
        size_raw = self.recv_exact(4)
        size = struct.unpack("!I", size_raw)[0]

        payload = self.recv_exact(size)
        return payload

    def send(self, payload: bytes):
        """Envia mensagem usando o mesmo socket persistente."""
        size = struct.pack("!I", len(payload))
        self.conn.sendall(size + payload)

    def recv_exact(self, n):
        data = b""
        while len(data) < n:
            chunk = self.conn.recv(n - len(data))
            if not chunk:
                raise ConnectionError("Conexão encerrada")
            data += chunk
        return data
