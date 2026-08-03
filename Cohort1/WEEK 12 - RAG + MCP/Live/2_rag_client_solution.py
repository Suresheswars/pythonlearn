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

import asyncio, json
from dotenv import load_dotenv, find_dotenv
from mcp import ClientSession
from mcp.client.sse import sse_client
from openai import OpenAI

load_dotenv(find_dotenv())
openai_client = OpenAI() #and pick MODEL = "gpt-4o-mini" (or similar)

SERVER_URL = "http://127.0.0.1:8010/sse"


async def list_server_tools(url: str):
     async with sse_client(url) as (read, write):
        async with ClientSession(read, write) as session:
               await session.initialize()
               return (await session.list_tools()).tools


async def call_server_tool(url: str, tool_name: str, tool_args: dict):
    """Connect to the server just long enough to call one tool."""
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
MODEL = "gpt-4o-mini"

async def run_agent(messages: list, openai_tools: list) -> str:
    """Answer the latest message in `messages`, calling learn_website / ask_question
    on the MCP server as needed. Appends its own turns onto `messages` so follow-up
    questions ("what else does it say about pricing?") resolve using conversation history."""

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
        print(f"  -> {tool_name}({tool_args})")

        try:
            result = await call_server_tool(SERVER_URL, tool_name, tool_args)
            result_text = result.content[0].text
        except Exception as e:
            result_text = f"Error calling {tool_name}: {e}"
        print(f"  <- {result_text[:300]}")

        messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result_text})

    # Turn 2: give the LLM the tool result so it can phrase a final answer.
    final_response = openai_client.chat.completions.create(model=MODEL, messages=messages)
    final_msg = final_response.choices[0].message
    messages.append({"role": "assistant", "content": final_msg.content})
    return final_msg.content


async def main():
    print("=" * 60)
    print("Website Knowledge RAG -- MCP Client")
    print("=" * 60)

    print("\nDiscovering tools from the server...")
    try:
        tools = await list_server_tools(SERVER_URL)
    except Exception as e:
        print(f"Could not connect to the server ({e}). Is 1_website_knowledge_server_master.py running?")
        return
    print(f"Tools available: {[t.name for t in tools]}")
    openai_tools = mcp_tools_to_openai_format(tools)

    print("\nReady! Type 'quit' to exit, 'reset' to forget the conversation so far.")
    print("Try: 'learn https://docs.python.org/3/tutorial/introduction.html'")
    print("then: 'what does the tutorial say about numbers?'")

    messages = []  # full conversation history, shared across turns

    while True:
        question = input("\nAsk (or tell me to learn a URL): ").strip()
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
        answer = await run_agent(messages, openai_tools)
        print(f"\nAnswer: {answer}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted.")
