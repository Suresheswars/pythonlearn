# Week 12 — RAG + MCP: Live Session Code

This is the **capstone** live session: it combines everything from the last
few weeks — RAG (Weeks 5-8) and MCP (Week 11) — into one end-to-end system.
Instead of a RAG pipeline living inside a notebook, the retrieval and
generation logic is exposed as **MCP tools**, so any MCP-compatible client
(our own script, or Claude Desktop) can crawl a website, remember what it
read, and answer questions about it.

Both files here are **fill-in-the-blanks** versions (`_student.py`) — build
them yourself using the `TODO`s and hints inline. There is no separate
`_solution.py` in this folder; the hints are detailed enough to get you to a
working system, and the goal is to type it out yourself rather than compare
against a finished copy.

## Learning objectives

By the end of this week you should be able to:

- Explain what an **embedding** is and why semantic search (nearest-neighbor
  over vectors) finds relevant text that plain keyword search would miss.
- Explain why documents are **chunked** before embedding, and what
  `chunk_size`/`chunk_overlap` actually control.
- Read and explain an **LCEL chain** (`{...} | prompt | llm | StrOutputParser()`)
  — what each stage receives and returns.
- Explain why a RAG prompt template constrains the LLM to answer **only from
  retrieved context**, and what fails if you skip that constraint.
- Expose an existing pipeline (RAG, in this case) as an **MCP tool**, and
  explain the difference between a *stateless* tool (Week 11) and a
  *stateful* one backed by a persistent store (this week).
- Explain the difference between the **stdio** and **SSE** transports and
  say, for any given client, which one it must use and why.

## Key concepts (glossary)

| Term | What it means here |
|---|---|
| **Embedding** | A numeric vector representation of a piece of text such that texts with similar *meaning* end up close together in vector space. `OpenAIEmbeddings(model="text-embedding-3-small")` turns each chunk (and later, each query) into one of these vectors. |
| **Vector store** | A database indexed for fast "find the vectors closest to this one" search instead of exact-match lookup. Chroma is the vector store here; `./chroma_website_knowledge` is where it persists its files to disk. |
| **Chunking** | Splitting a long document into smaller overlapping pieces before embedding, because (a) embedding models have a context limit and (b) retrieval is more precise over a focused paragraph than a whole page. `RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)` does this — see *why these numbers* below. |
| **Retriever / top-k** | The component that, given a query, embeds it and returns the `k` closest chunks from the vector store. `retriever = vector_store.as_retriever(search_kwargs={"k": 4})` returns the 4 best-matching chunks per question. |
| **RAG (Retrieval-Augmented Generation)** | Instead of asking the LLM to answer from memory, you retrieve relevant text first and paste it into the prompt, so the LLM answers from *your* data instead of (or in addition to) what it was trained on. |
| **LCEL (LangChain Expression Language)** | The `|` pipe syntax for chaining Runnables (`retriever \| prompt \| llm \| parser`) — see the full breakdown in the code walkthrough below. |
| **MCP tool** | A plain Python function annotated with `@mcp.tool()`. Its name, parameters, and docstring get sent to the LLM as a callable's "spec"; the LLM decides when to call it, based on nothing but that spec — which is why the docstrings matter as much as the code. |
| **Transport** | The mechanism MCP uses to move messages between client and server — see the stdio vs. SSE section below. It is independent of what the tools themselves do. |

## What this demo is

Two files, playing two different roles:

| File | Role | Port |
|---|---|---|
| `1_website_knowledge_server_student.py` | MCP **server** — the capstone. Exposes two tools: `learn_website(url)` and `ask_question(query)` | 8010 |
| `2_rag_client_student.py` | MCP **client / host** — the chat program you actually talk to | — |

The server owns the *entire* RAG pipeline behind two tools:

- **`learn_website(url)`** — crawl → chunk → embed → store. Every call
  **adds** to the same persistent Chroma collection instead of replacing it,
  so the knowledge base grows the more pages you teach it.
- **`ask_question(query)`** — retrieve → generate. Pulls the top-k matching
  chunks out of Chroma and asks an LLM to answer *only* from that context.

The client connects to the server, discovers its tools, hands them to an
OpenAI model, and lets the model decide when to call `learn_website` vs.
`ask_question` based on what you type.

```
                    ┌─────────────────────────┐
User types a         │  2_rag_client_student   │
question or ------>  │  (Host + Client +       │
"learn <url>"         │   OpenAI Agent)         │
                    └────────────┬────────────┘
                                 │ MCP over SSE (HTTP)
                                 ▼
                  1_website_knowledge_server
                          :8010
                                 │
                 ┌───────────────┼───────────────┐
                 ▼               ▼               ▼
          learn_website()  WebBaseLoader   ask_question()
          (crawl+chunk+     (crawler)      (retrieve+generate)
           embed+store)         │                │
                 └──────► Chroma vector store ◄──┘
                       (./chroma_website_knowledge,
                        persists across runs)
```

This mirrors the real architecture: **User Query → Agent → MCP Server →
Website Crawler → Vector DB (Chroma) → RAG Answer.**

## Prerequisites

1. Python 3.10+ with these packages installed:
   ```bash
   pip install mcp python-dotenv openai langchain-openai langchain-chroma \
               langchain-community langchain-text-splitters langchain-core
   ```
2. A `.env` file (in this folder, or anywhere above it — `find_dotenv()`
   searches upward) containing:
   ```
   OPENAI_API_KEY=sk-...
   ```
   The server checks for this key on startup and exits with a clear error
   instead of crashing confusingly mid-class inside `OpenAIEmbeddings` if
   it's missing.

## How to run it — 2 separate terminals

Same rule as Week 11: the server is a long-running process that has to stay
alive on its port, so it needs **its own terminal**.

```bash
# Terminal 1 — start the server first, leave it running
python 1_website_knowledge_server_student.py

# Terminal 2 — only after the server above is running
python 2_rag_client_student.py
```

On startup, the client connects to the server and lists what it found:

```
Discovering tools from server...
  learn_website: crawl a URL, chunk it, embed it, and add it to the knowledge base
  ask_question: answer a question using only what's been learned so far

Ready! Type 'quit' to exit, 'reset' to forget the conversation so far.

Ask a question:
```

Try this sequence:

1. `learn https://en.wikipedia.org/wiki/Retrieval-augmented_generation`
   → routed to `learn_website`; the server crawls the page, splits it into
   ~1000-character chunks, embeds them, and adds them to Chroma.
2. `What problem does RAG solve?`
   → routed to `ask_question`; the server retrieves the top 4 matching
   chunks and asks the LLM to answer from them only.
3. `learn <a second URL>`, then ask something that spans both pages — since
   `learn_website` **adds** rather than replaces, the knowledge base now
   covers both.
4. Ask something *not* covered by anything you've taught it — the prompt
   template instructs the LLM to say "I don't know" instead of making
   something up.

## Code walkthrough

### `1_website_knowledge_server_student.py`

- **Fail fast on missing config.** Checks `OPENAI_API_KEY` at import time and
  `sys.exit(1)`s with a clear message rather than letting the first tool
  call blow up inside `OpenAIEmbeddings`.
- **One persistent Chroma collection, shared by both tools.** Created once
  at module load (`collection_name="website_knowledge"`,
  `persist_directory="./chroma_website_knowledge"`), so it survives server
  restarts and every `learn_website()` call adds to the same store.
- **`learn_website(url)`**
  - Validates the URL starts with `http://`/`https://` before crawling —
    return a clear message instead of crawling garbage otherwise.
  - `WebBaseLoader(url, requests_kwargs={"timeout": 15}, raise_for_status=True)`
    — the timeout stops one slow site from hanging the whole call;
    `raise_for_status` makes a 404/500 fail loudly instead of silently
    "learning" an error page as if it were real content.
  - Splits with `RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)`,
    filters out empty/whitespace-only chunks, then
    `vector_store.add_documents(chunks)`.
  - Wrapped in `try/except` so a bad URL returns a message instead of
    crashing the server.

  **Why `chunk_size=1000, chunk_overlap=200`?** There's a direct tradeoff:
  - Too **small** a chunk size → each chunk lacks surrounding context, so the
    LLM gets fragments instead of coherent facts (e.g. a sentence split away
    from the paragraph that defines what "it" refers to).
  - Too **large** a chunk size → retrieval gets *less precise*, because a
    5000-character chunk about ten different sub-topics matches almost any
    query a little, instead of one chunk matching very well. It also wastes
    context-window space with irrelevant text once retrieved.
  - **Overlap** (200 chars here) exists so a fact sitting right at a chunk
    boundary doesn't get split in half with no single chunk containing it
    whole — the next chunk repeats the last 200 characters of the previous
    one as a safety margin.
  - `1000/200` is a reasonable default for prose (like Wikipedia articles),
    not a law — dense technical text or code often wants smaller chunks;
    long narrative text can tolerate larger ones. This is a knob you're
    meant to tune per use case, not a fixed constant.

  **Why `k=4` on the retriever?** Same tradeoff in a different place: too
  low a `k` risks missing the one chunk that actually answers the question;
  too high a `k` pads the prompt with marginally-relevant chunks, which
  costs tokens and can dilute the model's attention away from the chunk
  that matters. `k=4` is a starting point to tune against your own data.

- **`ask_question(query)`**
  - Classic RAG chain:
    `{"context": retriever, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser()`.
    Reading it left to right, LCEL-style:
    1. `{"context": retriever, "question": RunnablePassthrough()}` runs in
       parallel on the incoming `query` string: `retriever` embeds the query
       and fetches the top-`k` chunks (becomes `context`); `RunnablePassthrough()`
       just hands the original query straight through unchanged (becomes
       `question`). Output: `{"context": [...chunks...], "question": "..."}`.
    2. `| prompt` feeds that dict into `ChatPromptTemplate.from_template(ANSWER_TEMPLATE)`,
       which substitutes `{context}` and `{question}` into the template
       string below and produces a fully-formed prompt.
    3. `| llm` sends that prompt to `ChatOpenAI(model="gpt-4o-mini", temperature=0)`
       and gets back a chat completion (`temperature=0` because we want
       consistent, non-creative answers grounded in the context, not varied
       ones).
    4. `| StrOutputParser()` unwraps the raw completion object down to a
       plain string, which is what the tool returns to the client.
  - `ANSWER_TEMPLATE` is what actually enforces "answer only from context" —
    it isn't a magic model behavior, it's this explicit instruction:
    ```
    You are a helpful assistant that ONLY answers questions based on the provided context.

    STRICT RULES:
    1. ONLY use information from the context below.
    2. Do NOT use your general knowledge or training data.
    3. If the context doesn't contain the answer, respond with: "I don't know - this information wasn't found in the learned websites."
    4. Mention which website the answer came from when you can.

    Context from learned websites:
    {context}

    Question: {question}

    Answer (based ONLY on the context above):
    ```
    Rule 3 is exactly why "I don't know" shows up instead of a hallucinated
    guess — the model is being told explicitly what to do when retrieval
    comes up empty, not left to decide on its own.
- **Two transports, one server.** `mcp.run(transport="sse")` is what we use
  live so the client can connect over the network; swapping to
  `transport="stdio"` is what lets Claude Desktop launch this same script
  directly — see the step-by-step walkthrough below.

### `2_rag_client_student.py`

- Plain script, one top-level `asyncio.run()` — deliberately not a Jupyter
  notebook so there's no competing event loop to fight with.
- `list_server_tools()` / `call_server_tool()` both open a fresh
  `sse_client(url)` → `ClientSession` connection, matching the pattern from
  Week 11's multi-server client.
- `mcp_tools_to_openai_format()` reshapes MCP's tool schema into the
  `{"type": "function", "function": {...}}` shape the OpenAI API expects.
- `run_agent(messages, openai_tools)` is the two-turn tool-calling loop:
  call the LLM with `tool_choice="auto"` → if it wants a tool, call it via
  `call_server_tool()`, append a `{"role": "tool", ...}` message with the
  result → call the LLM again so it can phrase the final answer.
- `messages` is the **full conversation history**, created once outside the
  main loop and appended to every turn — exactly the pattern from Week 11 —
  which is what lets follow-up questions like "what else does it say?"
  resolve correctly. `reset` clears it; `quit` exits.

## API cost note

Both tools call the OpenAI API and cost money on every invocation:
`learn_website` embeds *every chunk* of the page (one embedding call per
chunk, batched), and `ask_question` makes one chat completion call. Crawling
ten large pages in a row for fun will burn through more tokens than you'd
expect — start with one or two smaller pages while you're still debugging.

## Section 5 — connecting this server to Claude Desktop (stdio walkthrough)

Everything above runs the server over SSE so our own `2_rag_client_student.py`
can connect to it. Claude Desktop can use the *exact same tools*, but it has
to launch the server itself, which means switching transports. Steps:

1. **Flip the transport in the server file.** Change the bottom of
   `1_website_knowledge_server_student.py` from
   `mcp.run(transport="sse")` to `mcp.run(transport="stdio")`. Only one of
   the two should be active at a time — SSE for our in-class client, stdio
   for Claude Desktop.
2. **Find your Python interpreter's full path** (Claude Desktop launches a
   specific executable, not whatever `python` resolves to in your shell):
   - macOS/Linux: `which python3`
   - Windows: `where python`
3. **Open Claude Desktop's config file**: Claude menu → Settings →
   Developer → Edit Config. This opens `claude_desktop_config.json`.
4. **Merge in the `mcpServers` entry** from
   `claude_desktop_config_snippet.json`, replacing `FULL_PATH_TO/...` with
   the absolute path to your `1_website_knowledge_server_student.py`, and
   `"command": "python"` with the full interpreter path from step 2 if
   `python` alone isn't on Claude Desktop's `PATH`:
   ```json
   {
     "mcpServers": {
       "website-knowledge": {
         "command": "python",
         "args": ["FULL_PATH_TO/1_website_knowledge_server_student.py"]
       }
     }
   }
   ```
5. **Fully quit and reopen Claude Desktop** (not just close the window) so it
   picks up the config change and launches the server.
6. **Verify it connected** — open a new chat in Claude Desktop and look for a
   tools/plug icon; `website-knowledge` with `learn_website` and
   `ask_question` should be listed. If it isn't, see Troubleshooting below.
7. **Test it** — ask Claude Desktop to learn a URL and then ask a question
   about it, the same way you did with `2_rag_client_student.py`. Claude
   Desktop is now acting as both the *host* and the *client*; your script is
   purely the *server*.

This is the moment that makes the stdio-vs-SSE distinction concrete: the
**identical tool code** runs under both transports — only the one line at the
bottom of the file, and who starts the process, changes.

## Interview prep — questions you should be able to answer cold

These are the kind of questions this week's material maps directly onto in
technical interviews. Try answering each in 2-3 sentences before checking
your own understanding against the sections above.

**RAG / embeddings / vector stores**
- What is RAG, and what problem does it solve that fine-tuning or a bigger
  context window doesn't (cheaply)?
- What is an embedding, and why does "cosine similarity between two
  embeddings" find semantically related text instead of just exact-keyword
  matches?
- Why do you chunk documents before embedding them, instead of embedding the
  whole document as one vector? What goes wrong at each extreme (chunks too
  small / too large)?
- What is `chunk_overlap` for, concretely — what failure does it prevent?
- What does the retriever's `k` control, and what's the cost of setting it
  too high vs. too low?
- Why does `ask_question` set `temperature=0`? What would change with
  `temperature=1`?
- How do you stop a RAG system from hallucinating when the answer isn't in
  the retrieved context? (Point to `ANSWER_TEMPLATE` rule 3 — this is prompt
  design, not a model setting.)
- Why is the vector store persistent (`persist_directory=...`) instead of
  in-memory here, and what would you lose if it were in-memory?

**MCP / tools / transports**
- What is MCP, in one sentence, and what problem does it solve for
  connecting LLMs to tools?
- What actually gets sent to the LLM to describe a tool? (Name, parameters,
  and docstring — the LLM never sees your function's implementation.)
- What is the difference between the stdio and SSE transports, and what's
  the deciding factor for which one a given client must use?
- Why can Claude Desktop only use stdio for a locally-scripted server like
  this one, while our own client uses SSE?
- What's the practical difference between exposing 4 separate single-tool
  servers (Week 11) versus 1 server exposing 2 tools (Week 12)? Is there a
  hard rule for how many tools belong on one server?
- If a tool call fails (bad URL, server down, missing API key), where should
  that be handled — inside the tool, or by the client? Why does this
  server's code catch exceptions *inside* `learn_website` rather than
  letting them propagate?

**System design / architecture**
- Walk through the full path of a single question from user input to final
  answer in this system (host → client → MCP protocol → server → retriever
  → LLM → back).
- Why does moving RAG logic behind an MCP tool (this week) make it usable
  from Claude Desktop, a Slack bot, or any other MCP-compatible client
  without rewriting the RAG code itself? What's the actual reusability being
  bought here?
- What would you change about this design to support multiple users with
  separate knowledge bases instead of one shared Chroma collection?

## Troubleshooting

- **"FAILED to connect" when starting the client** — the server isn't
  running yet, or isn't listening on port 8010. Start Terminal 1 first and
  confirm it's still alive.
- **`learn_website` returns an error immediately** — check the URL starts
  with `http://` or `https://`, and that the site doesn't block the default
  crawler user agent (this is why the server sets a custom `USER_AGENT`
  before importing `WebBaseLoader`).
- **`ask_question` keeps saying "I don't know"** — either nothing relevant
  has been learned yet (`learn_website` a page first), or the question is
  genuinely outside what's been crawled so far. This is the prompt working
  as intended, not a bug.
- **Port already in use** — a previous run of the server is still alive in
  another window; close it (or change `port=` in
  `1_website_knowledge_server_student.py`) before starting a new one.
- **Knowledge base feels "stuck" with stale content** — the Chroma store
  persists on disk at `./chroma_website_knowledge`. Delete that folder to
  start the knowledge base over from empty.
