import asyncio
import aio_pika # <--- Lembre-se: underline aqui!
import json
import time

async def criar_fila_teste():
    print("Tentando conectar ao RabbitMQ...")
    try:
        # 1. Conecta ao broker
        connection = await aio_pika.connect_robust(
            host="localhost",
            port=5672
        )
        
        async with connection:
            # 2. Abre o canal
            channel = await connection.channel()
            
            nome_da_fila = "news"
            queue = await channel.declare_queue(nome_da_fila, auto_delete=False)
            
            for i in range(10):
                        payload = json.dumps({
                            "pub_id": i+3,
                            "msg_id": i,
                            "sent_at": time.perf_counter()
                        }).encode()
                        await channel.default_exchange.publish(
                            aio_pika.Message(body=payload),
                            routing_key="news"
                        )
            
           

    except Exception as e:
        print(f"❌ Erro ao criar fila: {e}")

if __name__ == "__main__":
    asyncio.run(criar_fila_teste())