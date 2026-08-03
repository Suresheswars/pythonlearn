# ============================================================================
# 2_rag_client_student.py -- the Host + Client for the capstone demo.
# Build it yourself using the hints below.
#
# Plain script on purpose: one top-level asyncio.run(), no Jupyter kernel event
# loop to fight with. Run the server in its own terminal first:
#
#   python 1_website_knowledge_server_master.py   (or your own _student.py)
#
# then run this in a second terminal.
#
# Flow, matching the capstone architecture diagram:
#   User Query -> Agent -> MCP Server -> Website Crawler -> Vector DB (Chroma)
#              -> RAG Answer
# ============================================================================

# TODO: import asyncio, json
# TODO: from dotenv import load_dotenv, find_dotenv
# TODO: from mcp import ClientSession
# TODO: from mcp.client.sse import sse_client
# TODO: from openai import OpenAI

# TODO: load_dotenv(find_dotenv())
# TODO: create openai_client = OpenAI() and pick MODEL = "gpt-4o-mini" (or similar)

# TODO: SERVER_URL = "http://127.0.0.1:8010/sse"


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


# TODO: write async def run_agent(messages: list, openai_tools: list) -> str
# hint: messages is the FULL conversation history -- append your own turns
# onto it so follow-ups like "what else does it say?" resolve correctly
# hint: Turn 1 -- call the LLM with tools=openai_tools, tool_choice="auto"
# hint: if no tool_calls, append the assistant reply and return its content
# hint: otherwise, for each tool_call: call it via call_server_tool() and
# append a {"role": "tool", "tool_call_id", "content"} message with the result
# hint: Turn 2 -- call the LLM again with the updated messages so it can
# phrase a final answer using the tool result


# TODO: write async def main()
# hint: call list_server_tools(SERVER_URL) once at startup to discover tools;
# if the connection fails, print a helpful message and return
# hint: loop: input() a question, "quit" to break, "reset" to clear messages
# hint: append the question to messages, call run_agent(), print the answer
# hint: try "learn <a real URL>" first, then ask a question about it


# TODO: under if __name__ == "__main__": wrap asyncio.run(main()) in a
# try/except KeyboardInterrupt so Ctrl+C exits cleanly
