import asyncio
import time
import json
from multiprocessing import Process, Manager
from benchmark.metrics_colector import MetricsCollector
# Importe as funções ORIGINAIS do seu middleware aqui
from benchmark.my_mom.publisher.run_my_publisher import run_my_publisher
from benchmark.my_mom.subscriber.run_my_subscribers import run_my_subscriber

# --- CONFIGURAÇÕES DO TESTE (IDÊNTICAS AO RABBITMQ) ---
BROKER_HOST = "localhost"
BROKER_PORT = 5001  # A porta que o seu middleware usa
TOPIC = "news"
REPETICOES = 10
MSGS_POR_PUB = 1000
DURACAO_TESTE = 5 # segundos

# --- MAIN CONTROLLER ---
def executar_rodada_mymom(rodada_id):
    print(f"\n🚀 [MY_MOM] Iniciando Rodada {rodada_id}...")
    
    with Manager() as manager:
        shared_list = manager.list()
        # Inicializa o coletor com os mesmos parâmetros do teste do RabbitMQ
        collector = MetricsCollector(shared_list, 1, 1, "My_MOM", MSGS_POR_PUB)
        
        # 1. Inicia o Subscriber do seu Middleware
        # Ajustado para os nomes de argumentos que seu código usa
        p_sub = Process(
            target=run_my_subscriber, 
            kwargs={
                "sub_id": 1, 
                "topic": TOPIC, 
                "test_duration": DURACAO_TESTE, 
                "my_port": BROKER_PORT + 1, # Porta interna do sub se necessário
                "broker_host": BROKER_HOST, 
                "broker_port": BROKER_PORT, 
                "metrics_coletor": collector
            }
        )
        p_sub.start()
        
        time.sleep(1) # Aguarda o seu broker/subscriber estabilizar
        
        # 2. Inicia o Publisher do seu Middleware
        p_pub = Process(
            target=run_my_publisher, 
            kwargs={
                "pub_id": 1, 
                "topic": TOPIC, 
                "num_messages": MSGS_POR_PUB, 
                "broker_host": BROKER_HOST, 
                "broker_port": BROKER_PORT
            }
        )
        p_pub.start()
        
        # 3. Aguarda finalização
        p_pub.join()
        p_sub.join()
        
        # 4. Processa Resultados
        collector.process()
        report = collector.report(MSGS_POR_PUB, DURACAO_TESTE)
        print(f"📊 [MY_MOM] Resultado Rodada {rodada_id}: {report}")
        return report

if __name__ == "__main__":
    resultados_mymom = []
    
    # Inicia o seu Broker aqui se você tiver um comando Python para isso
    # Ex: p_broker = Process(target=iniciar_seu_broker); p_broker.start()

    for i in range(1, REPETICOES + 1):
        try:
            resultado = executar_rodada_mymom(i)
            resultados_mymom.append(resultado)
        except Exception as e:
            print(f"❌ Erro na rodada {i}: {e}")
        
        time.sleep(2) # Intervalo para limpeza de sockets do SO
    
    print("\n✅ Benchmark My_MOM concluído!")