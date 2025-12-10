# app/main.py
from fastapi import FastAPI, BackgroundTasks, WebSocket, WebSocketDisconnect, HTTPException
from .models import CreateGraphRequest, RunGraphRequest
from .engine.graph import engine
from .engine.registry import registry
from .storage import RunStore
from .workflows import code_review_async  # registers tools on import
import asyncio

app = FastAPI()

@app.post("/graph/create")
async def create_graph(req: CreateGraphRequest):
    # map node label -> function from registry
    nodes = {}
    for node_name, tool_name in req.nodes.items():
        func = registry.get(tool_name)
        if not func:
            raise HTTPException(status_code=400, detail=f"tool not found: {tool_name}")
        nodes[node_name] = func
    graph_id = await engine.create_graph(nodes, req.edges, req.start, concurrency=req.concurrency)
    return {"graph_id": graph_id}

@app.post("/graph/run")
async def run_graph(req: RunGraphRequest, background_tasks: BackgroundTasks):
    # start background run and return immediately (non-blocking)
    async def runner():
        await engine.run_graph(req.graph_id, req.initial_state)
    background_tasks.add_task(asyncio.create_task, runner())
    return {"status": "started"}

@app.post("/graph/run_sync")
async def run_graph_sync(req: RunGraphRequest):
    final_state, log, run_id = await engine.run_graph(req.graph_id, req.initial_state)
    return {"run_id": run_id, "final_state": final_state, "log": log}

@app.get("/graph/state/{run_id}")
async def get_state(run_id: str):
    data = await RunStore.get(run_id)
    if not data:
        raise HTTPException(status_code=404, detail="run not found")
    return data

# Optional: WebSocket for streaming logs live
class ConnectionManager:
    def __init__(self):
        self.conns = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.conns.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.conns.remove(websocket)

    async def broadcast(self, message):
        for ws in list(self.conns):
            try:
                await ws.send_json(message)
            except Exception:
                self.disconnect(ws)

manager = ConnectionManager()

@app.websocket("/ws/logs")
async def websocket_logs(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(ws)
