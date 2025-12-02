"""Demo server: creates broker, registers Calculator service and starts listening."""
import asyncio
from middleware.broker.broker_service import BrokerService
from middleware.broker.connection import BrokerConnection
from middleware.server.server_handler import ServerHandler
from app_demo.services import Calculator


async def main():
    broker = BrokerService()
    conn = BrokerConnection(broker)
    srv = ServerHandler(broker, queue="requests")
    srv.register_service(Calculator())

    print("Server started. Broker running in-process. Waiting for requests...")
    # keep running
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
