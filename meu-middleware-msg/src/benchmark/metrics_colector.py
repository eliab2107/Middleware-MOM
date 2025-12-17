
from statistics import mean
import time
import asyncio
class MetricsCollector:
    def __init__(self, shared_metrics_list, publishers, subscribers, middleware, messages):
        self.latencies = []
        self.total_messages_received = 0
        self.metrics  = shared_metrics_list
        self.latencies = []
        self.lock = asyncio.Lock()
        self.first_message_receive_at =float('inf')
        self.last_message_receive_at = float('-inf')
        self.publishers =publishers
        self.subscribers = subscribers
        self.middleware = middleware
        self.messages = messages
        
        
    def receive_metrics(self, metrics:dict):
        self.metrics.append(metrics)
        
        
    def process(self):
        for metric in self.metrics:
            self.latencies.append(metric["latencies"])
            self.total_messages_received += metric["messages"]
            self.first_message_receive_at = metric["first_message"] if metric["first_message"] < self.first_message_receive_at else self.first_message_receive_at
            self.last_message_receive_at = metric["last_message"] if metric["last_message"] >  self.last_message_receive_at else self.last_message_receive_at


    def report(self, sent: int, elapsed: float):
        lat = sorted(self.latencies)
        return {
            "middleware": self.middleware,
            "publishers": self.publishers,
            "subscribers": self.subscribers,
            "total_time":(self.last_message_receive_at - self.first_message_receive_at),
            "sent": self.messages,
            "total_messages_received": self.total_messages_received,
            "loss_rate": 1 - (self.total_messages_received / (self.messages*self.subscribers)) ,
            "throughput_msg_s": self.total_messages_received / (self.last_message_receive_at - self.first_message_receive_at),
            "lat_avg_ms": mean(lat) if lat else 0,
        }
