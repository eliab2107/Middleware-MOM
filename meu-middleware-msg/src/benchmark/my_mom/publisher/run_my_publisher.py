"""Demo client that uses the Proxy to call remote service methods."""
import asyncio
from middleware.client.proxy import ClientProxy 
from middleware.publisher.publisher import Publisher
import time

# --- run_my_publisher.py ---

import asyncio
import time
# ... from .middleware.client.publisher import Publisher # (Ou onde o Publisher está)

# 1. A Lógica Assíncrona (Renomeada)
async def publisher_async_main(publish_id, messages, broker_host, broker_port, topic):
    publisher = Publisher(broker_host, broker_port)
    await publisher.connect()
    i = 0
    for i in range(messages):
        message = {"publish_id": publish_id, "id": i, "sent_at": time.perf_counter()}
        await publisher.publish(topic, message)
        i+=1
        
# 2. A Função Síncrona (Target do Multiprocessing)
def run_my_publisher(publish_id, messages, broker_host, broker_port, topic):
    # A ÚNICA tarefa é rodar a corrotina
    asyncio.run(publisher_async_main(publish_id, messages, broker_host, broker_port, topic)) 

# O bloco __main__ agora chama a função síncrona, se necessário (Para testes)
if __name__ == "__main__":
    # Note que run_my_publisher não precisa do 'await'
    # Você teria que passar argumentos de teste aqui:
    # run_my_publisher(0, "localhost", 5001, "news") 
    pass