# Graph-Based Code Analysis API

A FastAPI application that provides a graph-based workflow system for code analysis.

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Using the API

Visit `http://localhost:8000/docs` to access the interactive API documentation (Swagger UI) where you can test all endpoints directly.

## API Endpoints

### 1. Create Graph Workflow

`POST /graph/create` - Create a new graph workflow

![Create Graph Endpoint](./Examples/api:graph:create.png)

**Example Response:**
![Create Response](./Examples/create%20%20Response.png)

### 2. Run Graph Workflow

`POST /graph/run` - Execute a graph workflow

![Run Graph Endpoint](./Examples/api:graph:run.png)

**Example Response:**
![Run Response](./Examples/run%20response.png)

### 3. Get Run State

`GET /graph/state/{run_id}` - Get the state of a workflow run

**Example Response:**
![Run ID Response](./Examples/run_id%20%20response.png)

## Available Node Functions

- `extract` - Extract functions from code
- `complexity` - Compute code complexity
- `issues` - Detect code issues
- `suggest` - Generate suggestions based on analysis

