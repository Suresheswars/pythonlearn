# ============================================================================
# 2_weather_solution.py -- ONE of FOUR independent MCP servers in this demo.
# Owns just the get_weather tool: calls the OpenWeatherMap API for a city's
# current conditions. Run this file on its own (python 2_weather_solution.py);
# it starts an HTTP server on port 8002 that the client
# (5_multi_server_client_solution.py) talks to over MCP/SSE. Needs
# OPENWEATHER_API_KEY in a .env file -- see the README in this folder.
# ============================================================================

import os
import requests

from dotenv import load_dotenv, find_dotenv
from mcp.server.fastmcp import FastMCP

# find_dotenv() -> this finds the .env file present anywhere within the folder
load_dotenv(find_dotenv())

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

mcp = FastMCP("WeatherServer", host = "127.0.0.1", port = 8002)

@mcp.tool()
def get_weather(city: str) -> dict:
    """
    Get the current weather forecast for a city.
    
    Use this whenever the user asks about weather, temperature, or forecast for a specific place. 
    Works for any city recognized by OpenWeatherMap.

    Args:
        city: the city name, eg., Mumbai, Delhi, Pairs, London
    """
    if not OPENWEATHER_API_KEY:
        return {"city": city, "error": "OPENWEATHER_API_KEY not set in .env"}
    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"} ,
            timeout = 10,
        )
        data = response.json()
        if response.status_code != 200:
            return {"city": city, "error": data.get("message", "weather loopup failed")}
        return {
            "city": city,
            "condition": data["weather"][0]["description"].capitalize(),
            "temp_c": data["main"]["temp"],
        }
    except requests.RequestException as e:
        return {"city": city, "error": f"weather lookup failed: {e}"}

if __name__ == "__main__":
    mcp.run(transport = "sse")