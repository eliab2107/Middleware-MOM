import asyncio
import aio_pika
import json
import time

async def run_rabbitmq_publisher_async(pub_id, topic, num_messages, broker_host, broker_port):
    try:
        connection = await aio_pika.connect_robust(
            host=broker_host,
            port=broker_port
        )

        async with connection:
            channel = await connection.channel()
            
            await channel.declare_queue(topic, auto_delete=False)

            print(f"[PUB {pub_id}] Iniciando envio de {num_messages} msgs...")
            
            for i in range(num_messages):
                payload = json.dumps({
                    "pub_id": pub_id,
                    "msg_id": i,
                    "sent_at": time.perf_counter()
                }).encode()
                await channel.default_exchange.publish(
                    aio_pika.Message(body=payload),
                    routing_key=topic
                )
            
            print(f"[PUB {pub_id}] Envio concluído.")

    except Exception as e:
        print(f"[PUB {pub_id}] Erro: {e}")

def run_my_publisher(pub_id, topic, num_messages, broker_host, broker_port):
    asyncio.run(run_rabbitmq_publisher_async(pub_id, topic, num_messages, broker_host, broker_port))