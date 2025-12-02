"""Invoker: calls service methods based on incoming Message."""
from middleware.protocol import Message
from typing import Any
import asyncio


class Invoker:
    def __init__(self, service: Any):
        self.service = service

    async def handle(self, message: Message) -> Message:
      """Receive a message, call and execute the correct method and return result"""
      ...