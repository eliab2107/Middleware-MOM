
from multiprocessing import Process
from benchmark.my_mom.publisher.run_my_publisher import run_publish_process

BROKER_HOST = "localhost"
BROKER_PORT = 9002
BASE_PORT = 5000
SUBSCRIBERS = 10

if __name__ == "__main__":
    processes = []

    for i in range(SUBSCRIBERS):
        p = Process(target=run_publish_process,args=(i, BROKER_HOST, BROKER_PORT ))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
