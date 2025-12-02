"""Requestor helper (thin wrapper)"""
from middleware.client.proxy import Proxy


class Requestor:
    def __init__(self, proxy: Proxy):
        self.proxy = proxy

    async def invoke(self, method: str, *args, **kwargs):
        return await self.proxy.call(method, *args, **kwargs)
