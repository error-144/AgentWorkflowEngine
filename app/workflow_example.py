

EXAMPLE_WORKFLOW = {
    "start": "extract",
    "nodes": {
        "extract": "extract",
        "complexity": "complexity",
        "issues": "issues",
        "suggest": "suggest"
    },
    "edges": {
        "extract": "complexity",
        "complexity": "issues",
        "issues": "suggest"
    }
}

EXAMPLE_INITIAL_STATE = {
    "code": """
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total

def process_order(order):
    # TODO: Add validation
    if order.status == 'pending':
        return calculate_total(order.items)
    return None
""",
    "quality_threshold": 80
}


def get_example_workflow():
    """Get example workflow configuration."""
    return EXAMPLE_WORKFLOW, EXAMPLE_INITIAL_STATE


if __name__ == "__main__":
    
    print("Example workflow configuration:")
    print(f"Workflow: {EXAMPLE_WORKFLOW}")
    print(f"\nExample initial state: {EXAMPLE_INITIAL_STATE}")

