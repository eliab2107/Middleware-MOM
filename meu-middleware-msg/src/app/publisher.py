"""Demo client that uses the Proxy to call remote service methods."""
import asyncio
from middleware.client.proxy import ClientProxy 
from middleware.publisher.publisher import Publisher
import time

async def main():
    
    publisher = Publisher("localhost", 5001)
    await publisher.connect()
    i = 0

    while True:
        message = {"id": i, "data": "Hello", "sent_at": time.time()}
        await publisher.publish("news", message)
        i+=1
        time.sleep(0.5)
        
if __name__ == "__main__":
    asyncio.run(main())
