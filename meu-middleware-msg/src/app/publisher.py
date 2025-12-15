"""Demo client that uses the Proxy to call remote service methods."""
import asyncio
from middleware.client.proxy import ClientProxy 

async def main():
    client = ClientProxy()
    client.connect("localhost", 5001)
    client.publish(topic="news", payload="Hello subscribers")
    

if __name__ == "__main__":
    asyncio.run(main())
