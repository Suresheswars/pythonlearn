# LearnWithSarvesh

LearnWithSarvesh is a learning repository that collects notebooks, projects, workshops, and cohort material around Python, data science, LangChain, RAG, MCP, and multi-agent workflows.

## Folder Structure

- [12-Week LangChain Cohort1](12-Week%20LangChain%20Cohort1/) - cohort material covering LangChain fundamentals, RAG, MCP, and multi-agent orchestration.
- [AI Engineer Ready - Cohort1](AI%20Engineer%20Ready%20-%20Cohort1/) - assignment and workshop material for the AI Engineer track.
- [AI Engineer Ready - Cohort2](AI%20Engineer%20Ready%20-%20Cohort2/) - second run of the AI Engineer track, same weekly structure and assignments.
- [Python for DataScience](Python%20for%20DataScience/) - notebooks for Python basics, data structures, control flow, and applied exercises.
- [webinars](webinars/) - recorded webinar and live session resources.
- [lws_logo.png](lws_logo.png) - repository branding asset.

## Inside The Cohort Folders

### 12-Week LangChain Cohort1

- `Capstone Project/` - end-to-end capstone work, including resume screening, knowledge-base chat, and multi-agent orchestration.
- `Week1 Introduction to LangChain & AI Workflows/` - introductory material.
- `Week 2 Working with Prompts, Chains & Memory/` - prompt, chain, and memory exercises.
- `Week 3 AI Resume Analyzer/` - resume analysis project.
- `Week 4 PDF Document Summarizer (RAG Project) (Introduce LangSmith here)/` - RAG summarization project.
- `Week 5 AI Email Assistant/` - email assistant project.
- `Week 6 YouTube Transcript Summarizer/` - transcript summarization project.
- `Week 7 Customer Support Chatbot/` - support chatbot project.
- `Week 8 MCP Part 1/` - first MCP module.
- `Week 9 MCP Part 2/` - second MCP module.
- `Week 10 - Multi-Agent Orchestration (Research Team)/` - multi-agent orchestration content.
- `Week 11_12 Multi-Agent Orchestration (Research Team) - Part2/` - continuation of the orchestration material.
- `Doubt Clearing Session 2/` - support and recap material.

### AI Engineer Ready - Cohort1

- `Assignment 1/` - assignment options and starter projects.
- `Assignment 2/` - applied project assignments such as the resume screener, RAG app, and multi-agent orchestrator.
- `WEEK 1 — Setup, Python, VS Code, Git, Jupyter/` - setup and tooling.
- `WEEK 2 — AI Foundations (LLMs, Transformers, BERT, GPT)/` - AI foundations.
- `WEEK 3 — LangChain Basics (Prompts, LLMs, Chains)/` - LangChain basics.
- `WEEK 4 - Memory, Tools, Agents (LangChain)/` - memory, tools, and agents.
- `WEEK 5 — RAG Fundamentals (Retrieval-Augmented Generation)/` - RAG fundamentals.
- `WEEK 6 — RAG Optimization + LLM Evaluation + LangSmith/` - RAG optimization and evaluation.
- `WEEK 7 — PROJECT 1 (Part 1) Production-Grade RAG System/` - building a production-grade RAG system.
- `WEEK 8 — PROJECT 1 (Part 2) RAGAS + Pydantic + Retry/` - evaluating RAG with RAGAS, structured output with Pydantic, retry logic.
- `Week 9 - LangGraph Foundations/` - introduction to LangGraph for stateful agent workflows.
- `WEEK 10 — Multi-Agent Systems (LangGraph)/` - multi-agent systems built on LangGraph.
- `WEEK 11- MCP & External Tool Systems/` - MCP fundamentals: four single-tool servers plus a multi-server client. See [Week 11 vs Week 12](#week-11-vs-week-12-mcp-deep-dive) below.
- `WEEK 12 - RAG + MCP/` - capstone combining RAG with MCP: a RAG pipeline exposed as MCP tools. See [Week 11 vs Week 12](#week-11-vs-week-12-mcp-deep-dive) below.

### AI Engineer Ready - Cohort2

- `Assignment 1/` - assignment options and starter projects.
- `Assignment 2/` - applied project assignments such as the resume screener, RAG app, and multi-agent orchestrator.
- `WEEK 1 — Setup, Python, VS Code, Git, Jupyter/` - setup and tooling.
- `WEEK 2 — AI Foundations (LLMs, Transformers, BERT, GPT)/` - AI foundations.
- `WEEK 3 — LangChain Basics (Prompts, LLMs, Chains)/` - LangChain basics.
- `WEEK 4 - Memory, Tools, Agents (LangChain)/` - memory, tools, and agents.
- `WEEK 5 — RAG Fundamentals (Retrieval-Augmented Generation)/` - RAG fundamentals.
- `WEEK 6 — RAG Optimization + LLM Evaluation + LangSmith/` - RAG optimization and evaluation.

### Python for DataScience

- Notebooks for Python basics, operators, conditionals, loops, functions, indexing, slicing, comprehensions, dictionaries, sets, and a final project wrap-up.

## Week 11 vs Week 12: MCP Deep Dive

Both weeks live in `AI Engineer Ready - Cohort1/` (and follow the same structure
in Cohort2 once it reaches that point) and both teach **MCP (Model Context
Protocol)** — the standard for exposing tools to an LLM over a client/server
connection. The difference is *what* gets exposed as a tool and *how many
moving parts* are involved.

### What changes between the two weeks

| Aspect | Week 11 — MCP & External Tool Systems | Week 12 — RAG + MCP |
|---|---|---|
| Theme | MCP fundamentals — many small, independent tools | Capstone — an entire RAG pipeline exposed as MCP tools |
| Servers | 4 separate single-tool servers (`calculator`, `get_weather`, `web_search`, `currency_convertor`), each its own process/port | 1 server exposing 2 tools (`learn_website`, `ask_question`) on one port |
| Client | One client that discovers tools across all 4 servers and routes each call to the server that owns it | One client that talks to the single RAG server |
| Tool statefulness | Stateless — each tool call is a pure function (add numbers, look up weather, convert currency) | Stateful — `learn_website` writes into a **persistent Chroma vector store** that `ask_question` reads back from, and it grows across calls |
| Underlying pipeline | None — each tool is a short, self-contained function | Full RAG chain: crawl → chunk → embed → store → retrieve → generate (the same RAG logic from Weeks 5–8, just moved behind a tool interface instead of living in a notebook) |
| Transport(s) used | SSE only — all 4 servers and the client run over `http://127.0.0.1:PORT` | Both SSE (for the in-class client demo) **and** stdio (so Claude Desktop can launch the server itself) — see transport table below |
| New concept taught | Discovering and routing tool calls across *multiple* independent servers | Exposing a *stateful, multi-step pipeline* as a tool, and picking the right transport for who's going to call it |

In short: **Week 11 teaches the MCP plumbing** (server, client, tool discovery,
routing, conversation memory) using deliberately simple, stateless tools so
the plumbing itself is the whole lesson. **Week 12 keeps that exact plumbing**
and swaps in one real, stateful workload — RAG — to show that "a tool" can be
as small as a calculator or as large as an entire retrieval pipeline; MCP
doesn't care either way.

### MCP transport types compared

MCP separates *what a tool does* from *how the client and server talk to each
other*. That "how" is the transport, and this repo's code touches three of
them:

| Transport | How it works | Who starts the server process | Best fit | Where it's used here |
|---|---|---|---|---|
| **stdio** (standard input/output) | The client itself spawns the server as a subprocess and exchanges MCP messages over that process's stdin/stdout pipes | The **client** (e.g. Claude Desktop) | Local tools running on the same machine as the client, with no ports or networking to manage — the client fully owns the server's lifecycle | Week 12 server's `transport="stdio"` option, wired up via `claude_desktop_config_snippet.json` so Claude Desktop can launch `1_website_knowledge_server.py` directly |
| **SSE** (Server-Sent Events over HTTP) | The server runs as its own long-lived process listening on a port; one or more clients connect to it over HTTP and receive a stream of events | The **developer/user**, ahead of time, in a separate terminal | Custom scripts/clients you write yourself, a server that must stay up independently of any one client, or be shared by multiple clients | Week 11's 4 servers + client; Week 12 server's `transport="sse"` option used for the in-class client demo |
| **Streamable HTTP** | The spec's newer single-endpoint replacement for SSE, supporting both plain request/response and streaming over one HTTP route | The **developer/user**, ahead of time | Production or cloud-hosted MCP servers reachable remotely | Not used in this repo's code yet, but the direction hosted MCP servers are moving |

### Why does Claude (Desktop) specifically need stdio, while our own clients use SSE?

It comes down to **who is responsible for starting the server process**, not
any technical superiority of one transport over another:

- **Claude Desktop spawns the server itself.** When you add an entry to
  `claude_desktop_config.json` (see `claude_desktop_config_snippet.json` in
  Week 12), you're telling Claude Desktop "run this exact command
  (`python 1_website_knowledge_server.py`) yourself." Claude Desktop starts
  it when it needs it, and owns its stdin/stdout — so stdio is the only
  transport option that fits: there's no independently-running server on a
  port for it to dial into, because *it* is the one bringing the process to
  life.
- **Our own client scripts don't spawn anything.** In both Week 11 and
  Week 12, we start each server manually in its own terminal *before*
  running the client. The client's job is only to connect to a server that's
  already alive at a fixed URL (`http://127.0.0.1:8001`, `:8010`, etc.).
  That server can outlive any single client connection, restart
  independently, or be shared by more than one client at once — which is
  exactly the model SSE (or streamable HTTP) supports, and stdio does not
  (stdio ties one server process to the one client that launched it).

So the rule of thumb this repo's code demonstrates: **if the client launches
the server, use stdio; if the server is already running independently and the
client just connects to it, use SSE/HTTP.** Week 12's server supports both at
once for exactly this reason — `transport="sse"` for the custom client we
build in class, `transport="stdio"` for Claude Desktop, same underlying
RAG tools either way.

## Purpose

This repository is organized so each learning path can be explored independently while keeping shared practice material in one place.

## Repository Note

Please do not push the contents of this repository unless it is explicitly approved for sharing.
