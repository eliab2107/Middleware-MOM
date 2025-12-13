"""Queue manager with TTL support."""
import asyncio
import time
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
        self.locks: Dict[str, asyncio.Lock] = {}
        self.global_lock = asyncio.Lock()


    async def ensure(self, name: str) -> None:
        """Create/declare a new exchange or topic"""
        if name in self.queues:
            return
        async with self.global_lock:
            if name in self.queues:
                return
            self.queues[name] = []
            self.locks[name] = asyncio.Lock()
        
            
    async def enqueue(self, name: str, message: Message) -> None:
        """Add a new message in the queue"""
        await self.ensure(name)
        async with self.locks[name]:
            self.queues[name].append(message)
    

    async def dequeue(self, name: str) -> Optional[Message]:
        """Return the oldest non-expired message, or None if none available."""
        await self.ensure(name)
        async with self.locks[name]:
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
        asyncio.run(self.ensure(queue))
    
    async def delete_expired_messages(self, queue: str) -> None:
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