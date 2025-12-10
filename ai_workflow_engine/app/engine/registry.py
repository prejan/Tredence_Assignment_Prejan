# app/engine/registry.py
from typing import Callable, Dict
class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Callable] = {}

    def register(self, name: str, func: Callable):
        self.tools[name] = func

    def get(self, name: str):
        return self.tools.get(name)

registry = ToolRegistry()
