# ============================================================================
# 1_calculator_student.py -- ONE of FOUR independent MCP servers in this demo.
# Owns just the calculator tool. Build it yourself using the hints below.
# ============================================================================

# TODO: from mcp.server.fastmcp import FastMCP

# TODO: create the server -- FastMCP("CalculatorServer", host="127.0.0.1", port=8001)
# hint: the name string shows up when a client asks "what server am I talking to?"


# TODO: write calculator(operation: str, a: float, b: float) -> float, decorated
# with @mcp.tool()
# hint: handle operation in {"add", "subtract", "multiply", "divide"}
# hint: guard divide-by-zero and raise a clear ValueError for it
# hint: raise a clear ValueError for any operation string you don't recognize
# hint: write a docstring an LLM could read to know exactly when/how to call
# this tool -- cover the code and ask "could a human figure it out from just this?"


# ============================================================================
# THREE WAYS TO RUN A SERVER (pick one for the real entry point)
# hint: Option A - mcp.run(transport="stdio") -- subprocess/pipes, one client only
# hint: Option B - mcp.run(transport="streamable-http") -- newer HTTP transport
# hint: Option C - mcp.run(transport="sse") -- what we use live in class, a real
# HTTP server multiple clients can connect to over the network at once
# ============================================================================

# TODO: under if __name__ == "__main__": call mcp.run(transport="sse")
