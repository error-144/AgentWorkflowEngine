"""Pydantic models for API requests and responses."""

from pydantic import BaseModel


class GraphCreate(BaseModel):
    """Request model for creating a new graph workflow."""
    start: str
    nodes: dict  # node_name → node_function_key
    edges: dict  # node_name → next_node


class GraphRun(BaseModel):
    """Request model for running a graph workflow."""
    graph_id: str
    initial_state: dict

