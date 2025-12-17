import asyncio
import time
import json
import aio_pika
from multiprocessing import Process, Manager
from benchmark.metrics_colector import MetricsCollector

from benchmark.my_mom.publisher.run_my_publisher    import run_my_publisher
from benchmark.my_mom.subscriber.run_my_subscriber  import run_my_subscriber
import asyncio
from multiprocessing import Manager 
from benchmark.controller import BenchmarkController
from benchmark.metrics_colector import MetricsCollector
import pandas as pd
import os 
from typing import Dict, Any, List
import csv
from benchmark.my_mom.publisher.run_my_publisher     import run_my_publisher
from benchmark.my_mom.subscriber.run_my_subscriber  import run_my_subscriber
from benchmark.rabbitMQ.publisher.run_amqp_publisher import run_rabbitmq_publisher_async
from benchmark.rabbitMQ.subscriber.run_amqp_subscriber import run_rabbitmq_subscriber_async

def adicionar_dicionario_csv(
    dados_linha: dict,
    nome_arquivo: str = "dados_exportados.csv"
) -> None:
   
    
    # 1. Obter o cabeçalho (nomes das colunas)
    # A ordem das chaves é importante, usamos list(dict.keys())
    # O Python 3.7+ garante que a ordem das chaves é a ordem de inserção.
    fieldnames = list(dados_linha.keys())
    
    # Verifica se o arquivo já existe
    arquivo_existe = os.path.exists(nome_arquivo)
    
    try:
        # 2. Abrir o arquivo no modo 'a' (append) para adicionar a linha.
        # newline='' é necessário no Python para evitar linhas em branco extras no CSV no Windows.
        with open(nome_arquivo, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # 3. Se o arquivo não existe, escreve o cabeçalho
            if not arquivo_existe:
                writer.writeheader()
                print(f"Arquivo '{nome_arquivo}' criado com cabeçalho.")
            
            # 4. Escreve a nova linha (os valores do dicionário)
            writer.writerow(dados_linha)
            print(f"Sucesso! Uma linha de dados adicionada a '{nome_arquivo}'.")
            
    except Exception as e:
        print(f"Ocorreu um erro ao escrever no arquivo CSV: {e}")
    


NUM_SUBS = 5        
NUM_PUBS = 1        
MSGS_POR_PUB = 10000
TOTAL_ESPERADO = MSGS_POR_PUB * NUM_PUBS

BROKER_HOST = "localhost"
BROKER_PORT = 5672
TOPIC = "benchmark_scale_queue"
DURACAO_TESTE = 5 


async def subscriber_logic(sub_id, metrics_coletor):
    connection = await aio_pika.connect_robust(host=BROKER_HOST, port=BROKER_PORT)
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=100)
        queue = await channel.declare_queue(TOPIC, auto_delete=True)
        
        async def callback(message: aio_pika.IncomingMessage):
            async with message.process():
                now = time.perf_counter()
                data = json.loads(message.body.decode())
                metrics_coletor.receive_metrics({
                    "sub_id": sub_id,
                    "latencies": now - data['sent_at'],
                    "messages": 1,
                    "first_message": now, "last_message": now
                })
        
        await queue.consume(callback)
        await asyncio.sleep(DURACAO_TESTE)

def run_sub(sub_id, metrics_coletor):
    asyncio.run(subscriber_logic(sub_id, metrics_coletor))

# --- LOGICA DO PUBLISHER (IGUAL) ---
async def publisher_logic(pub_id):
    connection = await aio_pika.connect_robust(host=BROKER_HOST, port=BROKER_PORT)
    async with connection:
        channel = await connection.channel()
        for i in range(MSGS_POR_PUB):
            payload = json.dumps({"sent_at": time.perf_counter()}).encode()
            await channel.default_exchange.publish(
                aio_pika.Message(body=payload), routing_key=TOPIC
            )

def run_pub(pub_id):
    asyncio.run(publisher_logic(pub_id))

# --- CONTROLLER ESCALÁVEL ---
def executar_rodada_escalavel(rodada_id):
    print(f"\n🚀 [RODADA {rodada_id}] Config: {NUM_PUBS} Pubs | {NUM_SUBS} Subs")
    
    with Manager() as manager:
        shared_list = manager.list()
        collector = MetricsCollector(shared_list, NUM_PUBS, NUM_SUBS, "RabbitMQ", TOTAL_ESPERADO)
        
        # 1. LANÇAR TODOS OS SUBSCRIBERS
        lista_subs = []
        for i in range(NUM_SUBS):
            p = Process(target=run_sub, args=(i, collector))
            p.start()
            lista_subs.append(p)
        
        time.sleep(0.1) # Tempo para todos os subs conectarem
        
        # 2. LANÇAR TODOS OS PUBLISHERS
        lista_pubs = []
        for i in range(NUM_PUBS):
            p = Process(target=run_pub, args=(i,))
            p.start()
            lista_pubs.append(p)
            
        # 3. AGUARDAR TODOS OS PUBLISHERS TERMINAREM O ENVIO
        for p in lista_pubs:
            p.join()
            
        # 4. AGUARDAR TODOS OS SUBSCRIBERS TERMINAREM A DURAÇÃO
        for p in lista_subs:
            p.join()
            
        # 5. PROCESSAR RESULTADOS
        collector.process()
        return collector.report(TOTAL_ESPERADO, DURACAO_TESTE)

if __name__ == "__main__":
    resultados = []
    for r in range(1, 30): 
        resultados.append(executar_rodada_escalavel(r))
        print(f"📊 Resultado: {resultados[len(resultados)-1]}")
        
    for resultado in resultados:
        adicionar_dicionario_csv(resultado, "Relatorio_Benchmark.csv")