"""FastAPI application with graph workflow endpoints."""

from fastapi import FastAPI, HTTPException
import uuid

from app.models import GraphCreate, GraphRun
from app.graph_engine import GRAPHS, RUNS, run_engine
from app.nodes import NODE_FUNCTIONS

app = FastAPI(title="Graph-Based Code Analysis API")


@app.post("/graph/create")
def create_graph(req: GraphCreate):
    """Create a new graph workflow."""
    graph_id = str(uuid.uuid4())

    # Validate node functions
    for n, fn in req.nodes.items():
        if fn not in NODE_FUNCTIONS:
            raise HTTPException(400, f"Unknown node function: {fn}")

    GRAPHS[graph_id] = req.dict()
    return {"graph_id": graph_id}


@app.post("/graph/run")
async def run_graph(req: GraphRun):
    """Execute a graph workflow."""
    graph = GRAPHS.get(req.graph_id)
    if not graph:
        raise HTTPException(404, "graph_id not found")

    run_id = str(uuid.uuid4())
    RUNS[run_id] = {"state": req.initial_state.copy(), "log": [], "done": False}

    await run_engine(graph, run_id, req.initial_state.copy())

    return {
        "run_id": run_id,
        "final_state": RUNS[run_id]["state"],
        "log": RUNS[run_id]["log"]
    }


@app.get("/graph/state/{run_id}")
def get_run_state(run_id: str):
    """Get the state of a workflow run."""
    run = RUNS.get(run_id)
    if not run:
        raise HTTPException(404, "run_id not found")
    return run

