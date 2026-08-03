# ============================================================================
# 3_web_search_solution.py -- ONE of FOUR independent MCP servers in this demo.
# Owns just the web_search tool: hits the Tavily search API for live web
# results. Run this file on its own (python 3_web_search_solution.py); it
# starts an HTTP server on port 8003 that the client
# (5_multi_server_client_solution.py) talks to over MCP/SSE. Needs
# TAVILY_API_KEY in a .env file -- see the README in this folder.
# ============================================================================

import os
import requests
from dotenv import load_dotenv, find_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv(find_dotenv())

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

mcp = FastMCP("WebSearchServer", host = "127.0.0.1", port = 8003)

@mcp.tool()
def web_search(query: str) -> list:
    """
    Search the live web for current information.

    Use this whenever the user asks something that needs up-to-date facts or
    news beyond your training data, e.g. "who won the match yesterday" or
    "latest news about the Mumbai monsoon".

    Args:
        query: the search query
    """
    if not TAVILY_API_KEY:
        return [{"error": "TAVILY_API_KEY not set in .env"}]
    try:
        response = requests.post(
            "https://api.tavily.com/search",
            json = {"api_key": TAVILY_API_KEY, "query": query, "max_results": 5},
            timeout = 15,
        )
        data = response.json()
        return [
            {"title": r["title"], "url": r["url"], "content": r["content"]}
            for r in data.get("results", [])
        ]
    except requests.RequestException as e:
        return [{"error": f"Web search failed: {e}"}]

if __name__ == "__main__":
    mcp.run(transport = "sse")