import socket
import struct


class ClientRequestHandler:
    def __init__(self, host="localhost", port=5000):
        self.host = host
        self.port = port

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None

    def send_receive(self, message: bytes) -> bytes:
        """
        Usa conexão persistente já aberta.
        """
        if not self.sock:
            raise RuntimeError("Conexão não aberta. Use .connect()")

        # ---- Envia ----
        size = struct.pack("!I", len(message))
        print(f"Enviando mensagem de tamanho {len(size)} bytes...")
        self.sock.sendall(size + message)

        # ---- Recebe ----
        resp_size_raw = self._recv_exact(4)
        resp_size = struct.unpack("!I", resp_size_raw)[0]

        response = self._recv_exact(resp_size)
        return response

    def _recv_exact(self, n):
        data = b""
        while len(data) < n:
            chunk = self.sock.recv(n - len(data))
            if not chunk:
                raise ConnectionError("Conexão encerrada pelo servidor")
            data += chunk
        return data
