# ============================================================================
# 5_multi_server_client_solution.py -- the Host + Client + Agent, all in one
# plain script. Connects to all four MCP servers below, asks each one what
# tools it exposes, hands the merged tool list to an OpenAI model, and routes
# every tool call the model makes to the right server. Keeps a running
# `messages` list as its conversation memory so follow-up questions
# ("convert 1 INR" -> "to which currency?" -> "USD") resolve correctly.
#
# Plain script on purpose: one top-level asyncio.run(), no Jupyter kernel event
# loop to fight with. Run each server in its own terminal first:
#
#   python 1_calculator_solution.py
#   python 2_weather_solution.py
#   python 3_web_search_solution.py
#   python 4_currency_convertor_solution.py
#
# then run this file in a fifth terminal. Full walkthrough in the README in
# this folder.
# ============================================================================

import json
import asyncio # asynchronous programming
import os

from dotenv import load_dotenv, find_dotenv
from mcp import ClientSession
from mcp.client.sse import sse_client
from openai import OpenAI

load_dotenv(find_dotenv())

openai_client = OpenAI()
MODEL = "gpt-4o-mini"

SERVERS = {
    "calculator": "http://127.0.0.1:8001/sse",
    "weather": "http://127.0.0.1:8002/sse",
    "web_search": "http://127.0.0.1:8003/sse",
    "currency": "http://127.0.0.1:8004/sse",
}

async def list_server_tools(url: str):
    """Connect to one server just long enough to ask tools it has"""
    async with sse_client(url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            return (await session.list_tools()).tools

async def call_server_tool(url: str, tool_name: str, tool_args: dict):
    """Connect to one server just long enough to call one tool."""
    async with sse_client(url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            return await session.call_tool(tool_name, tool_args)

def mcp_tools_to_openai_format(mcp_tools):
    """Convert MCP's tool list into the JSON schema OpenAI's tool-calling API expects."""
    return [
        {"type": "function", "function": {"name": t.name, "description": t.description, "parameters": t.inputSchema}}
        for t in mcp_tools
    ]

async def discover_all_tools():
    """Ask every server what tools it has, once, at startup."""
    print("\nDiscovering tools from all servers...")
    openai_tools = []
    tool_to_server = {}
    for name, url in SERVERS.items():
        try:
            tools = await list_server_tools(url)
            for t in tools:
                tool_to_server[t.name] = name
            openai_tools.extend(mcp_tools_to_openai_format(tools))
            print(f"  {name}: {[t.name for t in tools]}")
        except Exception as e:
            print(f"  {name}: FAILED to connect ({e}) - is it running?")
    return openai_tools, tool_to_server

async def run_agent(messages: list, openai_tools: list, tool_to_server: dict) -> str:
    """Answer the latest question in `messages`, using the rest of `messages` as conversation
    history. Appends its own turns onto `messages` so the next call remembers this one -- e.g.
    "convert 1 INR" -> "to which currency?" -> "USD" resolves correctly because the follow-up
    answer is read from the same list."""

    # Turn 1: let the LLM decide whether it needs a tool.
    response = openai_client.chat.completions.create(
        model=MODEL, messages=messages, tools=openai_tools, tool_choice="auto",
    )
    msg = response.choices[0].message

    if not msg.tool_calls:
        messages.append({"role": "assistant", "content": msg.content})
        return msg.content

    messages.append(msg.model_dump(exclude_none=True))

    for tool_call in msg.tool_calls:
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)
        server_name = tool_to_server[tool_name]
        print(f"  -> {tool_name}({tool_args}) on {server_name} server")

        try:
            result = await call_server_tool(SERVERS[server_name], tool_name, tool_args)
            result_text = result.content[0].text
        except Exception as e:
            result_text = f"Error calling {tool_name} on {server_name} server: {e}"
        print(f"  <- {result_text}")

        messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result_text})

    # Turn 2: give the LLM the tool result so it can phrase a final answer.
    final_response = openai_client.chat.completions.create(model=MODEL, messages=messages)
    final_msg = final_response.choices[0].message
    messages.append({"role": "assistant", "content": final_msg.content})
    return final_msg.content

# Entry point of the entire program:
async def main():
    print("=" * 60)
    print("Multi-Server MCP Client")
    print("=" * 60)

    openai_tools, tool_to_server = await discover_all_tools()

    if not tool_to_server:
        print("\nCould not connect to any servers. Make sure all four are running:")
        for name, url in SERVERS.items():
            print(f"  {name}: {url}")
        return

    print("\nReady! Type 'quit' to exit, 'reset' to forget the conversation so far.")

    messages = []  # full conversation history, shared across turns

    while True:
        question = input("\nAsk a question: ").strip()
        if question.lower() == "quit":
            print("Goodbye!")
            break
        if question.lower() == "reset":
            messages = []
            print("Conversation history cleared.")
            continue
        if not question:
            continue

        messages.append({"role": "user", "content": question})
        answer = await run_agent(messages, openai_tools, tool_to_server)
        print(f"\nAnswer: {answer}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted.")