"""Placeholder benchmarking script for the custom middleware.

This script is a starting point to measure round-trip latency and throughput.
"""
import asyncio
import time
from middleware.broker.broker_service import BrokerService
from middleware.broker.connection import BrokerConnection
from middleware.client.proxy import Proxy
from middleware.server.server_handler import ServerHandler
from app_demo.services import Calculator


async def run_roundtrip(n=1000):
    broker = BrokerService()
    conn = BrokerConnection(broker)
    srv = ServerHandler(broker, queue="requests")
    srv.register_service(Calculator())
    proxy = Proxy(conn, queue="requests")

    start = time.perf_counter()
    for i in range(n):
        r = await proxy.call("add", i, i)
    end = time.perf_counter()
    print(f"Performed {n} requests in {end-start:.3f}s, avg {(end-start)/n*1000:.3f} ms/request")


if __name__ == "__main__":
    asyncio.run(run_roundtrip(100))
