# Graph-Based Code Analysis API

A FastAPI application providing a graph-based workflow engine for code analysis.

## How to Run

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Start the server:**
```bash
uvicorn app.main:app --reload
```

3. **Access the API:**
- API: `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`

## What the Workflow Engine Supports

### Core Features

- **Sequential Execution**: Nodes execute in graph-defined order via edges
- **Conditional Branching**: Dynamic routing based on state (e.g., if `issues > 2`, jump to 'issues' node)
- **Loop Stop Conditions**: Execution stops when conditions are met (e.g., `quality >= threshold`)
- **State Threading**: Mutable state is passed between nodes
- **Execution Logging**: Captures node transitions and state snapshots

### Available Node Functions

- `extract` - Extract function names from code
- `complexity` - Calculate average function name complexity
- `issues` - Detect code issues (TODOs, long lines, tabs)
- `suggest` - Generate recommendations and quality score

### API Endpoints

- `POST /graph/create` - Create a new graph workflow
- `POST /graph/run` - Execute a graph workflow
- `GET /graph/state/{run_id}` - Get the state of a workflow run

## Example Workflow

See `app/workflow_example.py` for a complete example of a code analysis workflow.

## What Would Be Improved With More Time

1. **Persistence**: Add database storage for graphs and runs instead of in-memory storage
2. **Error Handling**: More robust error recovery and retry mechanisms
3. **Validation**: Enhanced input validation and schema checking for graph definitions
4. **Testing**: Comprehensive unit and integration tests
5. **Performance**: Async optimizations and caching for repeated operations
6. **Monitoring**: Add logging, metrics, and observability
7. **Graph Visualization**: API endpoint to visualize graph structure
8. **Node Library**: Expandable registry of node functions with plugin support
9. **State Management**: Version control for state snapshots and rollback capabilities
10. **Documentation**: OpenAPI schema improvements and more detailed examples
