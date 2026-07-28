# ============================================================================
# 2_weather_student.py -- ONE of FOUR independent MCP servers in this demo.
# Owns just the get_weather tool. Build it yourself using the hints below.
# ============================================================================

# TODO: import os, requests, and load_dotenv/find_dotenv from dotenv
# TODO: from mcp.server.fastmcp import FastMCP

# TODO: load the .env file (hint: load_dotenv(find_dotenv()))
# TODO: read OPENWEATHER_API_KEY with os.getenv()

# TODO: create the server -- FastMCP("WeatherServer", host="127.0.0.1", port=8002)


# TODO: write get_weather(city: str) -> dict, decorated with @mcp.tool()
# hint: if OPENWEATHER_API_KEY is missing, return a dict with an "error" key
# instead of crashing
# hint: call requests.get("https://api.openweathermap.org/data/2.5/weather",
# params={"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}, timeout=10)
# hint: check response.status_code before trusting the payload; on failure
# return {"city": city, "error": ...}
# hint: on success pull data["weather"][0]["description"] and data["main"]["temp"]
# hint: wrap the request in try/except requests.RequestException
# hint: write a docstring an LLM could read to know exactly when/how to call
# this tool


# TODO: under if __name__ == "__main__": call mcp.run(transport="sse")
# (same SSE pattern as 1_calculator_student.py)
