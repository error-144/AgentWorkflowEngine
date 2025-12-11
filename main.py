from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI(title="Graph-Based Code Analysis API")

TOOLS = {}
GRAPHS = {}
RUNS = {}

def register_tool(name):
    def wrapper(fn):
        TOOLS[name] = fn
        return fn
    return wrapper

@register_tool("extract_functions")
def extract_functions(code: str):
    funcs = []
    for line in code.splitlines():
        line = line.strip()
        if line.startswith("def ") and "(" in line:
            name = line.split("def ")[1].split("(")[0]
            funcs.append(name)
    return funcs

@register_tool("compute_complexity")
def compute_complexity(funcs):
    return sum(len(f) for f in funcs) // (len(funcs) or 1)

@register_tool("detect_issues")
def detect_issues(code: str):
    issues = 0
    for l in code.splitlines():
        if "TODO" in l or len(l) > 120 or "\t" in l:
            issues += 1
    return issues

@register_tool("suggestions")
def suggestions(complexity, issues):
    s = []
    if complexity > 10:
        s.append("Reduce function complexity.")
    if issues > 0:
        s.append("Fix detected code style issues.")
    if not s:
        s.append("Code looks good.")
    return s

async def node_extract(state):
    funcs = TOOLS["extract_functions"](state["code"])
    state["functions"] = funcs
    return state

async def node_complexity(state):
    comp = TOOLS["compute_complexity"](state["functions"])
    state["complexity"] = comp
    return state

async def node_issues(state):
    iss = TOOLS["detect_issues"](state["code"])
    state["issues"] = iss
    return state

async def node_suggest(state):
    sugg = TOOLS["suggestions"](state["complexity"], state["issues"])
    state["suggestions"] = sugg
    quality = max(0, 100 - state["complexity"] * 5 - state["issues"] * 10)
    state["quality"] = quality
    return state

NODE_FUNCTIONS = {
    "extract": node_extract,
    "complexity": node_complexity,
    "issues": node_issues,
    "suggest": node_suggest,
}

async def run_engine(graph, run_id, state):
    current = graph["start"]
    edges = graph["edges"]
    nodes = graph["nodes"]

    while True:
        RUNS[run_id]["current_node"] = current
        fn = NODE_FUNCTIONS[nodes[current]]
        state = await fn(state)
        RUNS[run_id]["log"].append({"node": current, "state": state.copy()})

        if state.get("issues", 0) > 2:
            current = "issues"
            continue
        
        if state.get("quality", 0) >= state.get("quality_threshold", 80):
            break
        
        current = edges.get(current)
        if not current:
            break
    
    RUNS[run_id]["state"] = state
    RUNS[run_id]["done"] = True

class GraphCreate(BaseModel):
    start: str
    nodes: dict
    edges: dict

class GraphRun(BaseModel):
    graph_id: str
    initial_state: dict

@app.post("/graph/create")
def create_graph(req: GraphCreate):
    graph_id = str(uuid.uuid4())
    for n, fn in req.nodes.items():
        if fn not in NODE_FUNCTIONS:
            raise HTTPException(400, f"Unknown node function: {fn}")
    GRAPHS[graph_id] = req.dict()
    return {"graph_id": graph_id}

@app.post("/graph/run")
async def run_graph(req: GraphRun):
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
    run = RUNS.get(run_id)
    if not run:
        raise HTTPException(404, "run_id not found")
    return run

