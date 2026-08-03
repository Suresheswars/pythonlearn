# ============================================================================
# 1_calculator_solution.py -- ONE of FOUR independent MCP servers in this demo.
# Owns just the calculator tool: add/subtract/multiply/divide two numbers.
# Run this file on its own (python 1_calculator_solution.py); it starts an
# HTTP server on port 8001 that the client (5_multi_server_client_solution.py)
# talks to over MCP/SSE. See the README in this folder for the full run order.
# ============================================================================

from mcp.server.fastmcp import FastMCP # FastMCP is Py-Framework that makes extremely easy to build MCP servers, clients, annd applications


mcp = FastMCP("CalculatorServer", host = "127.0.0.1", port = 8001)
# This creates a MCP server instance, clients can identify which server they are connected to;

@mcp.tool()
def calculator(operation: str, a: float, b: float) -> float:
    """Perform a basic arithmetic operation on two numbers.

    Use this whenever the user asks for a calculatio. eg., What is 12 times 12?
    or asks "add 5 plus 7"

    Args: 
        operation: one of "add", "subtract", "multiply", "divide"
        a: the first number
        b: the second number
    """
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by 0")
        return a / b
    else:
        raise ValueError(f"Unknown operation: {operation!r}. Use add, subract, multiply or divide")

if __name__ == "__main__":
    mcp.run(transport = "sse") # transport = "stdio"