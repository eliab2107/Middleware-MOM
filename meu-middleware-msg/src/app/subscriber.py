"""Demo server: creates broker, registers Calculator service and starts listening."""
import asyncio
from middleware.subscriber.subscriber import Subscriber
from middleware.subscriber.client_subscriber import SubscriberClient
from middleware.client.proxy import ClientProxy
from middleware.callback.callback import Callback

def task(message):
    print("Task received: ", message["payload"])

async def main():
    subscriber = Subscriber("localhost", 5001, "localhost", 9002, task)
    await subscriber.subscribe("news")
    await subscriber.start()
    
if __name__ == "__main__":
    asyncio.run(main())
