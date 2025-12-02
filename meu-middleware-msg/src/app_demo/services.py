"""Example business logic service(s)"""
import asyncio


class Calculator:
    def add(self, a: int, b: int) -> int:
        return a + b

    async def slow_multiply(self, a: int, b: int, delay: float = 0.5) -> int:
        await asyncio.sleep(delay)
        return a * b
