# ============================================================================
# 3_web_search_student.py -- ONE of FOUR independent MCP servers in this demo.
# Owns just the web_search tool. Build it yourself using the hints below.
# ============================================================================

# TODO: import os, requests, and load_dotenv/find_dotenv from dotenv
# TODO: from mcp.server.fastmcp import FastMCP

# TODO: load the .env file and read TAVILY_API_KEY with os.getenv()

# TODO: create the server -- FastMCP("WebSearchServer", host="127.0.0.1", port=8003)


# TODO: write web_search(query: str) -> list, decorated with @mcp.tool()
# hint: if TAVILY_API_KEY is missing, return [{"error": ...}] instead of crashing
# hint: call requests.post("https://api.tavily.com/search",
# json={"api_key": TAVILY_API_KEY, "query": query, "max_results": 5}, timeout=15)
# hint: build a list of {"title", "url", "content"} dicts from data["results"]
# hint: wrap the request in try/except requests.RequestException
# hint: write a docstring an LLM could read to know exactly when/how to call
# this tool (e.g. questions needing facts/news beyond training data)


# TODO: under if __name__ == "__main__": call mcp.run(transport="sse")
# (same SSE pattern as 1_calculator_student.py)
