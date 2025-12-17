import asyncio
import aio_pika  # Nome correto do módulo após pip install aio-pika
import json
import time

async def run_rabbitmq_subscriber_async(sub_id, topic, test_duration, broker_host, broker_port, metrics_coletor):
    try:
        # Conexão robusta (reconecta automaticamente se cair)
        connection = await aio_pika.connect_robust(
            host=broker_host,
            port=broker_port
        )

        async with connection:
            channel = await connection.channel()
            
            # Melhora a performance: define quantas mensagens o worker "puxa" por vez
            await channel.set_qos(prefetch_count=100)

            # Declara a fila (garante que ela exista)
            queue = await channel.declare_queue(topic, auto_delete=False)

            async def callback(message: aio_pika.IncomingMessage):
                async with message.process(): # Faz o ACK automático ao sair do bloco
                    now = time.perf_counter()
                    data = json.loads(message.body.decode())
                    
                    # Cálculo de métricas
                    latency = now - data['sent_at']
                    
                    metrics = {
                        "sub_id": sub_id,
                        "first_message": now, # O coletor tratará o menor valor como 'first'
                        "last_message": now,
                        "latencys": [latency], # O coletor geralmente espera uma lista
                        "messages": 1
                    }
                    metrics_coletor.receive_metrics(metrics)

            # Inicia o consumo
            print(f"[SUB {sub_id}] Conectado e ouvindo a fila: {topic}")
            await queue.consume(callback)

            # Mantém o subscriber vivo pela duração do teste
            await asyncio.sleep(test_duration)
            print(f"[SUB {sub_id}] Tempo esgotado. Finalizando...")

    except Exception as e:
        print(f"[SUB {sub_id}] Erro: {e}")

def run_my_subscriber(sub_id, topic, test_duration, my_port, broker_host, broker_port, metrics_coletor):
    # Ponto de entrada para o multiprocessing
    asyncio.run(run_rabbitmq_subscriber_async(sub_id, topic, test_duration, broker_host, broker_port, metrics_coletor))