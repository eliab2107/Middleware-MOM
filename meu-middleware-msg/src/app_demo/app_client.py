"""Demo client that uses the Proxy to call remote service methods."""
import asyncio
from middleware.broker.broker_service import BrokerService
from middleware.broker.connection import BrokerConnection
from middleware.client.proxy import Proxy


async def main():
    # In this demo we create the broker locally and use the connection.
    broker = BrokerService()
    conn = BrokerConnection(broker)

    # NOTE: For a proper demo, run app_server in a separate process that uses the same broker instance.
    # Here we simulate both in one process for convenience: register a simple service directly.
    from app_demo.services import Calculator
    from middleware.server.server_handler import ServerHandler
    srv = ServerHandler(broker, queue="requests")
    srv.register_service(Calculator())

    proxy = Proxy(conn, queue="requests")

    print("Calling remote add(2,3)")
    res = await proxy.call("add", 2, 3)
    print("Result:", res)

    print("Calling remote slow_multiply(4,5) with TTL 1000ms")
    res2 = await proxy.call("slow_multiply", 4, 5, ttl_ms=2000)
    print("Result:", res2)


if __name__ == "__main__":
    asyncio.run(main())
