"""Node functions and tools for code analysis."""

TOOLS = {}


def register_tool(name):
    """Decorator to register a tool function."""
    def wrapper(fn):
        TOOLS[name] = fn
        return fn
    return wrapper


# ----------------------- RULE-BASED HELPERS ------------

@register_tool("extract_functions")
def extract_functions(code: str):
    """Extract function names from code."""
    funcs = []
    for line in code.splitlines():
        line = line.strip()
        if line.startswith("def ") and "(" in line:
            name = line.split("def ")[1].split("(")[0]
            funcs.append(name)
    return funcs


@register_tool("compute_complexity")
def compute_complexity(funcs):
    """Calculate average function name complexity."""
    return sum(len(f) for f in funcs) // (len(funcs) or 1)


@register_tool("detect_issues")
def detect_issues(code: str):
    """Detect code issues: TODOs, long lines, tabs."""
    issues = 0
    for l in code.splitlines():
        if "TODO" in l or len(l) > 120 or "\t" in l:
            issues += 1
    return issues


@register_tool("suggestions")
def suggestions(complexity, issues):
    """Generate suggestions based on complexity and issues."""
    s = []
    if complexity > 10:
        s.append("Reduce function complexity.")
    if issues > 0:
        s.append("Fix detected code style issues.")
    if not s:
        s.append("Code looks good.")
    return s


# ----------------------- NODE FUNCTIONS ------------

async def node_extract(state):
    """Node: Extract functions from code."""
    funcs = TOOLS["extract_functions"](state["code"])
    state["functions"] = funcs
    return state


async def node_complexity(state):
    """Node: Compute code complexity."""
    comp = TOOLS["compute_complexity"](state["functions"])
    state["complexity"] = comp
    return state


async def node_issues(state):
    """Node: Detect code issues."""
    iss = TOOLS["detect_issues"](state["code"])
    state["issues"] = iss
    return state


async def node_suggest(state):
    """Node: Generate suggestions and quality score."""
    sugg = TOOLS["suggestions"](state["complexity"], state["issues"])
    state["suggestions"] = sugg
    
    # Derive quality score
    quality = max(0, 100 - state["complexity"] * 5 - state["issues"] * 10)
    state["quality"] = quality
    return state


NODE_FUNCTIONS = {
    "extract": node_extract,
    "complexity": node_complexity,
    "issues": node_issues,
    "suggest": node_suggest,
}

