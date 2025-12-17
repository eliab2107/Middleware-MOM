import asyncio
from middleware.subscriber.subscriber import Subscriber
import time
from typing import List, Dict
from benchmark.metrics_colector import MetricsCollector


async def run_my_subscriber_async(sub_id, topic, test_duration,  broker_host: str, broker_port: int, metrics_coletor:MetricsCollector, my_port: int):

        last_message = time.perf_counter()
        first_message = time.perf_counter()
        messages = 0
        latencies = []
        def task(message):
            nonlocal first_message, last_message, messages, latencies
            if messages == 0:
                first_message = time.perf_counter()
            latency = time.perf_counter() - message["payload"]['sent_at']
            latencies.append(latency)
            last_message = time.perf_counter()
            metrics = { "sub_id": sub_id,
                    "first_message": first_message,
                    "last_message": last_message,
                    "latencies": latency, 
                    "messages": 1
                }

            metrics_coletor.receive_metrics(metrics)
            
        subscriber = Subscriber(broker_host=broker_host,broker_port=broker_port, my_host="localhost", my_port=my_port, callback=task)
                               
        await subscriber.subscribe(topic)
    
 
        listener_task = asyncio.create_task(subscriber.start()) 
        
        sleep_task = asyncio.create_task(asyncio.sleep(test_duration-3))
        listener_task
        sleep_task
        
        print(f"[SUBSCRIBER {sub_id}] Iniciando teste por {test_duration}s...")
        
        done, pending = await asyncio.wait(
            [listener_task, sleep_task],
            return_when=asyncio.FIRST_COMPLETED
        )

        print(f"[SUBSCRIBER {sub_id}] Tempo de teste esgotado ({test_duration}s). Cancelando listener...")
        
        for task in pending:
            task.cancel()
        
        
def run_my_subscriber(sub_id, topic, test_duration, my_port: int, broker_host: str, broker_port: int, metrics_coletor:MetricsCollector):
    print("broker: ", broker_host, broker_port)
    asyncio.run(run_my_subscriber_async(sub_id, topic, test_duration, my_port, broker_host, broker_port, metrics_coletor))
        
        
        
if __name__ == "__main__":
    # Apenas execute a chamada principal aqui
    asyncio.run(run_my_subscriber()) 