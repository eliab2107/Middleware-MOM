from multiprocessing import Process
from benchmark.my_mom.subscriber.run_my_subscriber import run_my_subscriber

BROKER_HOST = "localhost"
BROKER_PORT = 9002
BASE_PORT = 5000
SUBSCRIBERS = 10

if __name__ == "__main__":
    processes = []

    for i in range(SUBSCRIBERS):
        p = Process(target=run_subscriber_process,args=(i, BASE_PORT + i, BROKER_HOST, BROKER_PORT ))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
