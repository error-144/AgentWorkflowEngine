"""Graph execution engine for workflow orchestration."""

from app.nodes import NODE_FUNCTIONS

GRAPHS = {}  # Store graph definitions
RUNS = {}    # Store run states and logs


async def run_engine(graph, run_id, state):
    """
    Execute a graph workflow.
    
    Supports:
    - Sequential execution based on graph edges
    - Conditional branching (e.g., if issues > 2, jump to 'issues' node)
    - Loop stop conditions (e.g., quality >= threshold)
    - State threading between nodes
    - Execution logging
    """
    current = graph["start"]
    edges = graph["edges"]
    nodes = graph["nodes"]

    while True:
        RUNS[run_id]["current_node"] = current

        # Run node
        fn = NODE_FUNCTIONS[nodes[current]]
        state = await fn(state)
        RUNS[run_id]["log"].append({"node": current, "state": state.copy()})

        # Conditional Branching
        if state.get("issues", 0) > 2:
            current = "issues"
            continue
        
        # Loop Stop Condition
        if state.get("quality", 0) >= state.get("quality_threshold", 80):
            break
        
        # Default next node
        current = edges.get(current)
        if not current:
            break
    
    RUNS[run_id]["state"] = state
    RUNS[run_id]["done"] = True

