from middleware.client.proxy import ClientProxy

class Publisher:
    """
    Publisher
    - Conecta ao broker
    - Publica eventos
    - NÃO recebe mensagens
    """

    def __init__(self, broker_host: str, broker_port: int ):
        self.client_proxy = ClientProxy(broker_host, broker_port)
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.connected = False


    async def connect(self):
        if not self.connected:
            await self.client_proxy.connect()
            self.connected = True
            

    async def publish(self, topic: str, message: bytes):
        """
        Publica um evento em um tópico.
        """
        if not self.connected:
            raise RuntimeError("Publisher não conectado ao broker")

        response = await self.client_proxy.publish(topic, message)
        return response  


    async def close(self):
        if self.connected:
            await self.client_proxy.close()
            self.connected = False
