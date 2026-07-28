# Week 11 -- MCP & External Tool Systems: Live Session Code

This folder holds the **completed, working code** we built together during the
live session. If you want the fill-in-the-blanks version to practice on your
own first, use the `Students_totry` folder instead -- same five files, but
with `TODO`s and hints instead of finished code. Come back here to compare
your solution or to see the reference implementation run end-to-end.

## What this demo is

A tiny multi-agent tool system built on **MCP (Model Context Protocol)**.
MCP is a standard way to expose "tools" (plain Python functions) to an LLM
over a network connection, so the LLM can decide when to call them and use
their results to answer a question.

There are **five files**, playing two different roles:

| File | Role | Port |
|---|---|---|
| `1_calculator_solution.py` | MCP **server** -- exposes a `calculator` tool | 8001 |
| `2_weather_solution.py` | MCP **server** -- exposes a `get_weather` tool (OpenWeatherMap) | 8002 |
| `3_web_search_solution.py` | MCP **server** -- exposes a `web_search` tool (Tavily) | 8003 |
| `4_currency_convertor_solution.py` | MCP **server** -- exposes a `currency_convertor` tool | 8004 |
| `5_multi_server_client_solution.py` | MCP **client / host** -- the chat program you actually talk to | -- |

Each server is a **separate, independent process** that knows about exactly
one tool. The client is a separate process too: it connects to all four
servers, asks each "what tools do you have?", hands the combined list to an
OpenAI model, and whenever the model wants to use a tool, forwards that call
to whichever server owns it. This mirrors how real MCP setups work -- tools
can live anywhere (different machines, different teams, different languages)
and the client/agent just needs their URLs.

```
                     ┌───────────────────────┐
                     │  5_multi_server_client │   <- you type questions here
                     │   (Host + Client +     │
                     │    OpenAI Agent)       │
                     └───────────┬────────────┘
                                 │  MCP over SSE (HTTP)
         ┌──────────────┬───────┴───────┬──────────────┐
         ▼              ▼               ▼               ▼
  1_calculator   2_weather       3_web_search   4_currency_convertor
   :8001            :8002            :8003            :8004
```

## Prerequisites

1. Python 3.10+ with these packages installed:
   ```
   pip install mcp requests python-dotenv openai
   ```
2. A `.env` file (in this folder, or anywhere above it -- `find_dotenv()`
   searches upward) containing:
   ```
   OPENAI_API_KEY=sk-...
   OPENWEATHER_API_KEY=...
   TAVILY_API_KEY=...
   ```
   - No `OPENWEATHER_API_KEY` / `TAVILY_API_KEY`? Those two servers still run
     fine -- their tools just return a friendly `{"error": ...}` instead of
     crashing, so you can still demo the calculator and currency converter.
   - `OPENAI_API_KEY` is required -- the client can't run without it.

## How to run it -- 5 separate terminals

**This is the most important part to get right.** Each server is its own
long-running process that has to stay alive and keep listening on its port,
so **every server needs its own terminal window**. If you run them one after
another in the same terminal, the first one blocks and the rest never start.

Open **five terminals** in this folder and run one command in each, in this
order:

```bash
# Terminal 1
python 1_calculator_solution.py

# Terminal 2
python 2_weather_solution.py

# Terminal 3
python 3_web_search_solution.py

# Terminal 4
python 4_currency_convertor_solution.py

# Terminal 5 -- only after the four servers above are running
python 5_multi_server_client_solution.py
```

The four servers print nothing dramatic -- they just sit there listening
(e.g. on `http://127.0.0.1:8001`). That's correct; leave them running.

The client (terminal 5) is the one you actually interact with. On startup it
connects to all four servers and prints what it found:

```
Discovering tools from all servers...
  calculator: ['calculator']
  weather: ['get_weather']
  web_search: ['web_search']
  currency: ['currency_convertor']

Ready! Type 'quit' to exit, 'reset' to forget the conversation so far.

Ask a question:
```

If a server isn't running yet, the client will tell you it "FAILED to
connect" for that one and carry on with the rest -- so you'll know exactly
which terminal to check.

Try asking things like:
- "What is 12 times 7?" -> routed to the calculator server
- "What's the weather in Mumbai?" -> routed to the weather server
- "Convert 50 USD to INR" -> routed to the currency server
- "Who won the match yesterday?" -> routed to the web search server

Watch terminal 5's output: it prints which tool it called, on which server,
and what came back, before the model turns that into a final answer.

## Why the `messages` list matters (the "memory" block)

Look at `main()` in `5_multi_server_client_solution.py`:

```python
messages = []  # full conversation history, shared across turns

while True:
    question = input("\nAsk a question: ").strip()
    ...
    messages.append({"role": "user", "content": question})
    answer = await run_agent(messages, openai_tools, tool_to_server)
```

`messages` is created **once, outside the loop**, and every turn appends to
it instead of replacing it. `run_agent()` also appends the assistant's
replies and every tool call/result onto the same list. That list is passed
back into the OpenAI call on the *next* turn too.

This is what gives the client **conversational memory**. Without it, every
question would be answered in total isolation -- the model would have no idea
what you asked two seconds ago. With it, this works:

```
Ask a question: Convert 1 INR
  -> the model doesn't have a target currency yet, so it asks you for one
Answer: Sure -- which currency would you like to convert 1 INR to?

Ask a question: USD
  -> "USD" alone is meaningless without history, but because `messages`
     still holds the original "Convert 1 INR" question, the model knows
     exactly what you mean
  -> currency_convertor({'amount': 1, 'from_currency': 'INR', 'to_currency': 'USD'}) on currency server
Answer: 1 INR is approximately 0.01 USD.
```

Without shared history, the second turn ("USD") would be a dead end -- the
model would have nothing to attach it to. This is also why the tool call and
its result get appended to `messages` too (not just the plain-text answer):
the model needs to see *what it already tried and what it got back* so it
doesn't repeat a tool call or contradict itself on the next turn.

Two commands let you control this memory directly:
- `reset` -- sets `messages = []`, wiping the conversation so far. Use this
  when you want to start a fresh topic without restarting the whole client.
- `quit` -- exits the program. Since `messages` only lives in memory (it's
  never written to disk), it's gone as soon as the process ends -- this demo
  has no long-term memory across restarts, only within a single run.

## Troubleshooting

- **"Could not connect to any servers"** when starting the client -- none of
  the four server terminals are running yet. Start them first.
- **A tool call errors out with a connection error** -- the server that owns
  that tool crashed or was closed. Check its terminal.
- **Weather/search tools return `{"error": "...API_KEY not set in .env"}`**
  -- add the missing key to your `.env` file and restart that one server.
- **Port already in use** -- a previous run of that server is still alive in
  another window; close it (or change the `port=` in that file) before
  starting a new one.
