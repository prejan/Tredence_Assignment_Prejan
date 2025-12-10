# app/engine/graph.py
import uuid, asyncio
from typing import Dict, Any, Optional
from .node import Node
from ..storage import GraphStore, RunStore
from concurrent.futures import ProcessPoolExecutor

class Graph:
    def __init__(self, nodes: Dict[str, Node], edges: Dict[str, str], start: str, concurrency: int = 5):
        self.nodes = nodes
        self.edges = edges
        self.start = start
        self.semaphore = asyncio.Semaphore(concurrency)
        # executor for blocking tasks (threadpool handled inside Node)
        self.process_executor: Optional[ProcessPoolExecutor] = None

    def set_process_executor(self, executor: ProcessPoolExecutor):
        self.process_executor = executor

    async def execute_node(self, node: Node, state: Dict[str, Any], timeout: int = 30):
        async with self.semaphore:
            try:
                # If node function requires heavy CPU can decide to run in process executor externally
                return await asyncio.wait_for(node.run(state, executor=None), timeout=timeout)
            except asyncio.TimeoutError:
                state.setdefault("errors", []).append(f"{node.name}: timeout")
                return state

    async def execute(self, initial_state: Dict[str, Any]):
        state = dict(initial_state)
        log = []
        current = self.start

        while current:
            node = self.nodes[current]
            state = await self.execute_node(node, state)
            log.append({"node": current, "state": dict(state)})  # copy for log

            # basic loop/branch example
            if state.get("loop") is True:
                continue
            current = self.edges.get(current)
        return state, log

class GraphEngine:
    def __init__(self):
        self.process_executor = ProcessPoolExecutor()  # use for CPU offload if needed

    async def create_graph(self, nodes, edges, start, concurrency=5):
        graph_id = str(uuid.uuid4())
        node_objs = {name: Node(name, func) for name, func in nodes.items()}
        graph = Graph(node_objs, edges, start, concurrency)
        graph.set_process_executor(self.process_executor)
        await GraphStore.save(graph_id, graph)
        return graph_id

    async def run_graph(self, graph_id, initial_state):
        run_id = str(uuid.uuid4())
        await RunStore.init(run_id, initial_state)
        graph = await GraphStore.get(graph_id)
        if graph is None:
            raise KeyError("Graph not found")
        final_state, log = await graph.execute(initial_state)
        await RunStore.complete(run_id, final_state, log)
        return final_state, log, run_id

engine = GraphEngine()
