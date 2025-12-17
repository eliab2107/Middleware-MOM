
from benchmark.metrics_colector import MetricsCollector

from multiprocessing import Process
import time
class BenchmarkController:
    def __init__(self,  total_messages: int, topic: str, total_subscribers:int, total_publishers:int, total_time, metrics_controller:MetricsCollector,  target_publishers, target_subscribers, middleware):
        self.total_messages = total_messages
        self.topic = topic
        self.total_time = total_time
        self.metrics_coletor = metrics_controller
        self.total_subscribers = total_subscribers
        self.total_publishers =  total_publishers
        self.subscriber_processes = []
        self.topic = "news"
        self.broker_host = "localhost"
        self.broker_port = 5001
        if middleware == "rabbitMQ":
            self.broker_port = 5672
        self.all_processes = []
        self.target_subscribers = target_subscribers
        self.target_publishers = target_publishers
        
    async def run(self):
        for i in range(self.total_subscribers):
            p = Process(target=self.target_subscribers, args=(i, self.topic, 100,  self.broker_host, self.broker_port, self.metrics_coletor, self.broker_port+1+i))
            
            self.all_processes.append(p)
            p.start()
        time.sleep(2)
        for i in range(self.total_publishers):
            p = Process(target=self.target_publishers, args=(i, self.total_messages, self.broker_host, self.broker_port, self.topic))
            self.all_processes.append(p)
            p.start()

        return 0
    
    
    def wait_for_completion(self):
        
        import time
        
        print(f"[BENCHMARK] Esperando a duração do teste ({self.total_time} segundos)...")
        time.sleep(self.total_time*2)

    
        for p in self.all_processes:
            if p.is_alive():
                p.terminate() 
                print(f"[BENCHMARK] Processo {p.pid} forçadamente encerrado.")
        
        for p in self.all_processes:
            p.join(timeout=1) 
        print("[BENCHMARK] Todos os processos encerrados.")
    
    
    def process(self):
        self.metrics_coletor.process()
        return self.metrics_coletor.report(self.total_messages, self.total_time)