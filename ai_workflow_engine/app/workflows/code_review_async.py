# app/workflows/code_review_async.py
from ..engine.registry import registry
import asyncio

async def extract_functions(state):
    # simulated I/O-bound extraction
    await asyncio.sleep(0)  # yield control
    code = state.get("code", "")
    state["functions"] = code.count("def ")
    return state

def check_complexity(state):
    state["complexity"] = state.get("functions", 0) * 2
    return state

def detect_issues(state):
    state["issues"] = max(1, state.get("complexity", 0) // 3)
    return state

async def suggest_improvements(state):
    await asyncio.sleep(0)
    state["quality_score"] = 100 - state.get("issues", 0) * 10
    state["loop"] = state["quality_score"] < state.get("threshold", 80)
    return state

registry.register("extract", extract_functions)
registry.register("complexity", check_complexity)
registry.register("issues", detect_issues)
registry.register("improve", suggest_improvements)
