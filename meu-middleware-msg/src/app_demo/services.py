"""Example business logic service(s)"""
import asyncio


class Calculator:
    def add(self, a: float, b: float) -> float:
        return a + b


    def sub(self, a: float, b: float) -> float:
        return a - b

    
    def mult(self, a: float, b: float) -> float:
        return a * b


    def div(self, a: float, b:float) -> float:
        return a / b