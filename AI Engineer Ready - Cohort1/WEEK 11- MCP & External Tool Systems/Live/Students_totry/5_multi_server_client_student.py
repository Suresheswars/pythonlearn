# ============================================================================
# 5_multi_server_client_student.py -- the Host + Client + Agent, all in one
# plain script. Build it yourself using the hints below.
#
# Plain script on purpose: one top-level asyncio.run(), no Jupyter kernel event
# loop to fight with. Run each server in its own terminal first:
#
#   python 1_calculator_master.py   (or your own 1_calculator_student.py)
#   python 2_weather_master.py
#   python 3_web_search_master.py
#   python 4_currency_convertor_master.py
#
# then run this in a fifth terminal.
# ============================================================================

# TODO: import asyncio, json, os
# TODO: from dotenv import load_dotenv, find_dotenv
# TODO: from mcp import ClientSession
# TODO: from mcp.client.sse import sse_client
# TODO: from openai import OpenAI

# TODO: load_dotenv(find_dotenv())
# TODO: create openai_client = OpenAI() and pick MODEL = "gpt-4o-mini" (or similar)

# TODO: define SERVERS, a dict mapping server name -> its SSE URL
# hint: "http://127.0.0.1:<port>/sse" for ports 8001-8004


# TODO: write async def list_server_tools(url: str)
# hint: async with sse_client(url) as (read, write):
#           async with ClientSession(read, write) as session:
#               await session.initialize()
#               return (await session.list_tools()).tools


# TODO: write async def call_server_tool(url: str, tool_name: str, tool_args: dict)
# hint: same connect pattern as list_server_tools, but call
# await session.call_tool(tool_name, tool_args) instead


# TODO: write mcp_tools_to_openai_format(mcp_tools)
# hint: reshape each MCP tool into
# {"type": "function", "function": {"name", "description", "parameters": t.inputSchema}}


# TODO: write async def discover_all_tools()
# hint: loop over SERVERS, call list_server_tools() on each
# hint: build tool_to_server (tool name -> server name) and the merged
# openai-formatted tool list; print what each server has, or that it failed
# to connect


# TODO: write async def run_agent(messages: list, openai_tools: list, tool_to_server: dict) -> str
# hint: messages is the FULL conversation history (shared across turns) --
# append your own turns onto it so follow-up questions resolve correctly
# hint: Turn 1 -- call the LLM with tools=openai_tools, tool_choice="auto"
# hint: if no tool_calls, just append the assistant reply and return its content
# hint: otherwise, for each tool_call: look up its owning server in
# tool_to_server, call it via call_server_tool(), and append a
# {"role": "tool", "tool_call_id", "content"} message with the result
# hint: Turn 2 -- call the LLM again with the updated messages so it can
# phrase a final answer using the tool result


# TODO: write async def main()
# hint: call discover_all_tools() once at startup; if no servers connected,
# print a helpful message listing SERVERS and return
# hint: loop: input() a question, "quit" to break, "reset" to clear messages
# hint: append the question to messages, call run_agent(), print the answer


# TODO: under if __name__ == "__main__": wrap asyncio.run(main()) in a
# try/except KeyboardInterrupt so Ctrl+C exits cleanly
