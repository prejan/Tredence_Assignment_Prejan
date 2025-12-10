# app/storage.py
from typing import Dict, Any
import asyncio

class GraphStore:
    graphs: Dict[str, Any] = {}
    lock = asyncio.Lock()

    @classmethod
    async def save(cls, graph_id, graph):
        async with cls.lock:
            cls.graphs[graph_id] = graph

    @classmethod
    async def get(cls, graph_id):
        async with cls.lock:
            return cls.graphs.get(graph_id)

class RunStore:
    runs: Dict[str, Any] = {}
    lock = asyncio.Lock()

    @classmethod
    async def init(cls, run_id, initial_state):
        async with cls.lock:
            cls.runs[run_id] = {"state": initial_state, "log": [], "status": "running"}

    @classmethod
    async def complete(cls, run_id, final_state, log):
        async with cls.lock:
            cls.runs[run_id].update({"state": final_state, "log": log, "status": "completed"})

    @classmethod
    async def get(cls, run_id):
        async with cls.lock:
            return cls.runs.get(run_id)
