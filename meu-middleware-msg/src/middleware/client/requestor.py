"""Requestor helper (thin wrapper)"""
from middleware.client.proxy import Proxy


class Requestor:
    def __init__(self, proxy: Proxy):
       """Class to serialize calls"""

    async def invoke(self, method: str, *args, **kwargs):
        return await self.proxy.call(method, *args, **kwargs)
