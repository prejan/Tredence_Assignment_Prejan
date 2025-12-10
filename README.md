# Tredence_Assignment_Prejan
#  AI Workflow Engine (Async FastAPI + LangGraph-Style Graph Execution)

This project implements a fully asynchronous **AI Workflow Engine** inspired by LangGraph, capable of executing tool-based agent workflows using a **graph-based execution model** with:

- **Nodes** → represent functions (tools)
-  **Edges** → define execution flow
-  **Shared State** → state passed & mutated across nodes
-  **Looping / Branching Support**
-  **Async Execution with asyncio + FastAPI**
-  **In-memory Graph & Run Storage**
-  Optional WebSocket Log Streaming (real-time node updates)

#Architecture Diagram
<img width="1672" height="863" alt="image" src="https://github.com/user-attachments/assets/8a8add6e-86fd-4c2d-a342-60c514dd910e" />

#Graph Visualizer 
<img width="1763" height="875" alt="image" src="https://github.com/user-attachments/assets/6d81d42b-e091-4512-a6b5-4b457fcd95cd" />

#  Features

###  Async-first Node Execution
- Supports both **async** and **sync** functions.
- Sync functions are offloaded to threadpool (`run_in_executor`) so they **do not block the event loop**.

###  Graph Engine
- Create workflow graphs dynamically.
- Execute workflows step-by-step.
- Maintain logs of each node execution.
- Supports branching & loop conditions.

###  API Endpoints (FastAPI)
- `POST /graph/create` → Build a workflow graph.
- `POST /graph/run_sync` → Run and wait for final output.
- `POST /graph/run` → Background execution.
- `GET /graph/state/{run_id}` → Check execution status.

###  Tool Registry
- Simple global registry to register custom tools/functions.

###  Example Workflow (Code Review Mini-Agent)
Tools include:
- `extract` → count functions
- `complexity` → compute complexity score
- `issues` → detect code issues
- `improve` → compute quality score + loop logic

---

#  Project Structure
```bash
ai_workflow_engine/
│
├── app/
│ ├── main.py
│ ├── models.py
│ ├── storage.py
│ ├── engine/
│ │ ├── node.py
│ │ ├── graph.py
│ │ └── registry.py
│ └── workflows/
│ └── code_review_async.py
│
├── requirements.txt
└── README.md
```
#  Installation

```bash
git clone <your-repo-url>
cd ai_workflow_engine
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
# Run The Server
uvicorn app.main:app --reload --port 8000


#Create Graph
``` bash
POST /graph/create
{
  "nodes": {
    "n1": "extract",
    "n2": "complexity",
    "n3": "issues",
    "n4": "improve"
  },
  "edges": {
    "n1": "n2",
    "n2": "n3",
    "n3": "n4"
  },
  "start": "n1",
  "concurrency": 5
}
```
Output
``` bash
{
  "graph_id": "38533710-8141-46a8-871f-24b5e9d9aba1"
}
```
#Run Workflow Synchronously
``` bash
POST /graph/run_sync
{
  "graph_id": "38533710-8141-46a8-871f-24b5e9d9aba1",
  "initial_state": {
    "code": "def a(): pass\ndef b(): pass",
    "threshold": 80
  }
}
```
Output
```bash
{
  "run_id": "34a80292-55f9-4504-bb8b-089e01ff9dcb",
  "final_state": {
    "code": "def a(): pass\ndef b(): pass",
    "threshold": 80,
    "functions": 2,
    "complexity": 4,
    "issues": 1,
    "quality_score": 90,
    "loop": false
  },
  "log": [
    {"node": "n1", "state": {"functions": 2}},
    {"node": "n2", "state": {"complexity": 4}},
    {"node": "n3", "state": {"issues": 1}},
    {"node": "n4", "state": {"quality_score": 90, "loop": false}}
  ]
}
```
# Check Run State
``` bash
GET /graph/state/34a80292-55f9-4504-bb8b-089e01ff9dcb
```
Output
```bash
{
  "state": {
    "code": "def a(): pass\ndef b(): pass",
    "threshold": 80,
    "functions": 2,
    "complexity": 4,
    "issues": 1,
    "quality_score": 90,
    "loop": false
  },
  "log": [
    { "node": "n1", "state": {"functions":2} },
    { "node": "n2", "state": {"complexity":4} },
    { "node": "n3", "state": {"issues":1} },
    { "node": "n4", "state": {"quality_score":90, "loop":false} }
  ],
  "status": "completed"
}
```
#Outputs
<img width="1471" height="370" alt="image" src="https://github.com/user-attachments/assets/3d4f23e6-2d8c-4fe5-9df7-03d888cdcdb1" />

<img width="1919" height="1002" alt="image" src="https://github.com/user-attachments/assets/c3d916fe-5bfb-490c-b7a6-b605e84f38c3" />
<img width="1919" height="1018" alt="image" src="https://github.com/user-attachments/assets/92583b46-6625-4368-ae97-75ef68407f09" />
<img width="1446" height="706" alt="image" src="https://github.com/user-attachments/assets/cb4e254a-db50-401d-b490-c11e053082d4" />
<img width="1592" height="1007" alt="image" src="https://github.com/user-attachments/assets/3dc99e55-7394-4104-b0fb-20eb2376abb1" />
<img width="1643" height="1007" alt="image" src="https://github.com/user-attachments/assets/e21b12d4-f547-46ad-9d78-e8a3a3b84954" />







