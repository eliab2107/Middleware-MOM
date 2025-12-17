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
    dados_linha: Dict[str, Any],
    nome_arquivo: str = "dados_exportados.csv"
) -> None:
    """
    Adiciona os dados de um dicionário como uma nova linha a um arquivo CSV.
    Cria o arquivo com cabeçalho se ele não existir.

    Args:
        dados_linha: O dicionário contendo os dados de UMA linha,
                     onde as chaves são os nomes das colunas (cabeçalho).
                     Ex: {'Run_ID': 1, 'Latencia_Media_ms': 5.23}.
        nome_arquivo: O nome do arquivo CSV de saída.
    """
    
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
    
    
async def main(config):
    
    with Manager() as manager:
        shared_metrics_list = manager.list()
        messages    = config[0]
        publishers  = config[1]
        subscribers = config[2]
        time        = config[3]
        middleware  = config[4]
        target_publishers = config[5]
        target_subscribers = config[6]
        
        controller_coletor = MetricsCollector(shared_metrics_list, publishers, subscribers, middleware, messages) 
        
        controller = BenchmarkController(messages, "news", publishers, subscribers, time, controller_coletor, target_publishers, target_subscribers, middleware) 
        
        await controller.run() 
        controller.wait_for_completion()
    
        controller_coletor.process() 
        results = controller_coletor.report(10,10)
        adicionar_dicionario_csv(
        dados_linha=results,
        nome_arquivo="Relatorio_Benchmark.csv",
        )
        print(controller_coletor.report(10,10)) 
        
if __name__ == "__main__":
    config_tiers = [
        # Mensagens, Consumidores, Publishers, Duração (segundos), middleware, target_publisher, target_subscribe
        #(1000, 1, 1, 5, "my_mom", run_my_publisher, run_my_subscriber),     
        (1000, 1, 1, 5, "rabbitMQ", run_rabbitmq_publisher_async, run_rabbitmq_subscriber_async),  
        #(5000, 2, 1, 10),    
        #(10000, 4, 2, 15, "my_mom", run_my_publisher, run_my_subscriber),    
        #(20000, 8, 4, 20),    
        #(30000, 12, 6, 25),   
    ]
    for config in config_tiers:
        #for i in range(3):
        asyncio.run(main(config))



