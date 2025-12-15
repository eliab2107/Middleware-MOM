import asyncio
from typing import Dict, List, Any


class SubscriptionManager:
    def __init__(self):
        self.subscribers: Dict[str, List[Any]] = {}
        self.locks: Dict[str, asyncio.Lock] = {}
        self.global_lock = asyncio.Lock()

        
    async def ensure(self, topic):
        if topic in self.subscribers: 
            return
        async with self.global_lock: 
            if topic in self.subscribers:
                return
            self.subscribers[topic] = []
            self.locks[topic]       = asyncio.Lock()
        
        
    async def add_subscriber(self, topic, subscriber):
        await self.ensure(topic)
        async with self.locks[topic]:
            self.subscribers[topic].append(subscriber)

    async def remove_subscriber(self, topic, subscriber):
        await self.ensure(topic)
        async with self.locks[topic]:
            if topic in self.subscribers and subscriber in self.subscribers[topic]:
                self.subscribers[topic].remove(subscriber)

    def get_subscribers(self, topic):
        if topic not in list(self.subscribers.keys()):
            return []
        subscribers = self.subscribers[topic]   
        return subscribers
