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
        await publisher.publish("news", f"Hello subscribers{i}")
        i+=1
        time.sleep(0.5)
        
if __name__ == "__main__":
    asyncio.run(main())
