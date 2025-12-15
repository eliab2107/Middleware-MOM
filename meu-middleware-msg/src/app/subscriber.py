"""Demo server: creates broker, registers Calculator service and starts listening."""
import asyncio
from middleware.subscriber.subscriber import Subscriber
from middleware.client.proxy import ClientProxy


def task(message):
    print("Task received:", message)

async def main():
    client_proxy = ClientProxy()
    subscriber = Subscriber(client_proxy, "localhost", 9002, "localhost", 5001, task)
    
    subscriber.subscribe("news")
    await subscriber.start_server()
    
if __name__ == "__main__":
    asyncio.run(main())
