"""Queue manager with TTL support."""
import asyncio
from threading import Lock
from typing import Dict, List, Optional
from utils.protocol import Message

#Precisa de uma thread que esteja o tempo inteiro retirando e enviando as mensagens das filas, deve ser executada uma para cada fila(Notification Consumer) 
#Uma função para estar recebendo as mensagens e colocando na fila correta.
#Ambas as funções devem ser executadas para cada fila criada.

##Essas funções vão usar o invoker tanto para receber quanto para enviar as mensagens.
class QueueManager:
    def __init__(self):
        """Init manager queues"""
        # queue_name -> list of Message
        self.queues: Dict[str, List[Message]] = {}
        self.locks: Dict[str, Lock] = {}
        self.global_lock = asyncio.Lock()


    def ensure(self, name: str) -> None:
        """Create/declare a new exchange or topic"""
        if name in self.queues:
            print("haha")
            return
        else:
            self.locks[name] = Lock()
            self.locks[name].acquire()
            self.queues[name] = []
            self.locks[name].release()
        print("self.queues:", self.queues)
        print("queue created:", name, " : ", self.queues[name])
            
        
            
    def enqueue(self, name: str, message: Message) -> None:
        """Add a new message in the queue"""
        print("enqueueing message to", name, ":", message.payload)
        self.ensure(name)
        print("Current queue state:", self.queues[name])
        print("Acquiring lock for", self.locks[name])
        with self.locks[name]:
            self.queues[name].append(message)
            print(self.queues[name])
    

    def dequeue(self, name: str) -> Optional[Message]:
        """Return the oldest non-expired message, or None if none available."""
        self.ensure(name)
        with self.locks[name]:
            queue = self.queues[name]
            while queue:
                message = queue[0]
                if message.is_expired():
                    queue.pop(0)
                    continue
                return queue.pop(0) #Aqui a gente ta apagando a mensagem da fila antes de receber um ack.
            return None
    
    def get_queues(self) -> List[str]:
        """Return the list of existing topics/queues."""
        return list(self.queues.keys())
    
    
    def create_queue(self, queue: str) -> None:
        """Create a new queue."""
        self.ensure(queue)
    
    def delete_expired_messages(self, queue: str) -> None:
        """Remove expired messages from the specified queue."""
        if queue not in self.queues:
            return
        with self.locks[queue]:
            messages_to_delete = []
            for message in self.queues[queue]:
                if message.is_expired():
                    messages_to_delete.append(message)
                    
            for message in messages_to_delete:
                self.queues[queue].remove(message)