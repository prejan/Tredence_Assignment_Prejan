# app/models.py
from pydantic import BaseModel
from typing import Dict, Any

class CreateGraphRequest(BaseModel):
    nodes: Dict[str, str]  # mapping node_name -> registered tool name
    edges: Dict[str, str]
    start: str
    concurrency: int = 5

class RunGraphRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]
