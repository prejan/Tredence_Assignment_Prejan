# app/engine/node.py
import asyncio
from typing import Callable, Dict, Any
from inspect import iscoroutinefunction

class Node:
    def __init__(self, name: str, func: Callable[[Dict], Dict]):
        self.name = name
        self.func = func
        self.is_async = iscoroutinefunction(func)

    async def run(self, state: Dict[str, Any], *, executor=None) -> Dict[str, Any]:
        """
        Run the node function and return new state.
        If func is synchronous, run in threadpool (or provided executor).
        """
        if self.is_async:
            return await self.func(state)
        loop = asyncio.get_running_loop()
        # run sync functions in a threadpool to avoid blocking event loop
        return await loop.run_in_executor(executor, lambda: self.func(state))
