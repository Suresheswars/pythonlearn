# Week 9 — LangGraph Foundations

Up to now, every workflow you've built has been **linear**: a prompt goes into a chain, the chain
calls the LLM, the LLM's output comes out the other end. Even AgentExecutor (Week 4) — which *looks*
like it makes decisions — is really just a loop hidden inside one black-box object.

This week introduces **LangGraph**: a way of describing your AI workflow as an explicit graph of
**nodes** (steps) and **edges** (the paths between steps), with a shared **state** that flows through
the whole thing. Once you can see the graph, you can branch, loop, inspect every intermediate step,
and recover from failure — things that are awkward or impossible with plain chains or AgentExecutor.

By the end of this week you should be able to explain *why* LangGraph exists, not just how to call its
functions.

---

## 📂 What's in this folder

| File | What it teaches |
|---|---|
| `1. Week9_LangGraph_Foundations_Student.ipynb` | LangGraph from first principles: state, nodes, edges, compiling, running, streaming, and a classic state-handling bug |
| `1. Week9_LangGraph_Foundations_Student_totry.ipynb` | Same notebook, for you to fill in yourself (`_totry` = your working copy) |
| `2. Week9_Chains_AgentExecutor_vs_LangGraph_Student_totry.ipynb` | Builds the *same* tool-using agent three ways — LCEL chain, AgentExecutor, LangGraph — so you can see exactly where each one breaks down |

**Start with notebook 1, then do notebook 2.** Notebook 1 teaches the vocabulary; notebook 2 puts that
vocabulary to work by comparing LangGraph against the two tools you already know.

---

## 1️⃣ Why LangGraph Exists

To understand LangGraph, you first need to feel the pain of what came before it.

**LCEL Chains (`prompt | llm | parser`)** are great when your workflow is a straight line: step 1 always
leads to step 2, which always leads to step 3. The moment you need a *decision* — "if this is a math
question, do X, otherwise do Y" — you reach for `RunnableBranch`. That works for a single fork, but
chains have no concept of going *back*. You can't loop. If step 3 needs to ask step 1 to try again,
you're stuck.

**AgentExecutor** solves the looping problem by hiding a `while` loop inside itself: call the LLM, see
if it wants to use a tool, run the tool, feed the result back, repeat. This is powerful, but it's a
**black box**:

- You can't easily see what happened between steps (you have to dig through `verbose=True` logs or
  `return_intermediate_steps`).
- You can't change *how* it decides to continue — the looping logic is baked into the class.
- Its only safety valve against infinite loops is `max_iterations`, which just **silently cuts off**
  the agent mid-thought when it's reached. There's no clean signal that something went wrong — you just
  get a truncated answer.

**LangGraph** takes the loop that AgentExecutor was hiding and makes it an **explicit, visible graph**.
The same ReAct-style agent becomes: an `agent` node, a `tools` node, and a conditional edge that decides
whether to loop back to `agent` or stop. Nothing is hidden:

- `graph.stream(...)` lets you watch every node fire, one at a time.
- Adding a new tool means adding it to a list — the graph structure never changes.
- Going in a runaway loop raises a catchable `GraphRecursionError` instead of quietly truncating output.
- Because state is just a typed dictionary, you can persist it, replay it, or hand it to a human for
  approval mid-graph (you'll see more of this in later weeks — multi-agent systems are built entirely
  on top of these foundations).

Notebook 2 makes this concrete: you'll build the *exact same* "calculator + weather" agent as an LCEL
chain, as an AgentExecutor, and as a LangGraph graph, and watch each one hit its own wall.

---

## 2️⃣ Core LangGraph Concepts (the mental model)

Hold onto this mental model — everything else in LangGraph is a variation on it:

| Concept | What it is | Analogy |
|---|---|---|
| **State** | A `TypedDict` describing all the data flowing through your graph | A shared clipboard every step can read and write to |
| **Node** | A plain Python function: `(state) -> dict of updates` | One station on an assembly line |
| **Edge** | A connection telling the graph which node runs next | The conveyor belt between stations |
| **Conditional edge** | An edge whose destination is decided by a function, at runtime | A fork in the conveyor belt with a sensor deciding left or right |
| **START / END** | Special sentinel nodes marking where the graph begins and finishes | The "in tray" and "out tray" |
| **`StateGraph`** | The builder object you use to wire nodes and edges together | The blueprint for the assembly line |
| **`.compile()`** | Turns your builder into a runnable graph | Actually building the assembly line from the blueprint |
| **`.invoke(state)`** | Runs the graph start to finish, returns the final state | Push one item through the whole line, get the finished product |
| **`.stream(state)`** | Runs the graph but yields control back to you after *every* node | Watching the item move from station to station |

A node **never mutates the state object directly** — it returns a small dictionary of *only the fields
it's updating*. LangGraph takes that dictionary and merges it into the overall state before handing it
to the next node. This is the single most important — and most easily misunderstood — rule in LangGraph.

---

## 3️⃣ Understanding Graph State (and the bug everyone hits once)

In notebook 1 you define a state like this:

```python
class GraphState(TypedDict):
    query: str
    retrieved_docs: List[str]
    reasoning_steps: List[str]
    final_answer: str
```

Every node receives the *entire* state dict but should only return the keys it's actually changing.
For simple values (a string, a number) this is intuitive — return the new value and it overwrites the
old one.

**For lists, it is not automatic merging — it's a full replace.** If a node returns
`{"reasoning_steps": ["did step X"]}`, LangGraph doesn't append `"did step X"` to the existing list — it
**replaces** `reasoning_steps` entirely with a brand-new one-item list. Anything that was already in
there is gone.

That's why the correct pattern is always:

```python
return {"reasoning_steps": state["reasoning_steps"] + ["did step X"]}
```

— explicitly read the old list out of `state` and build a new list that includes it.

Notebook 1 has you build this bug *on purpose* (a "broken" version of the graph that overwrites instead
of appends) so you can see the symptom with your own eyes: by the end of the broken graph, you should
have 4 reasoning steps logged, but you'll only find 1. This is one of the most common real-world
LangGraph bugs — now you'll recognize it instantly.

(In notebook 2 you'll meet the cleaner alternative: `Annotated[List[BaseMessage], add_messages]`, a
*reducer* that tells LangGraph "for this field, append automatically instead of replacing." More on
reducers in later weeks.)

---

## 4️⃣ Building Your First LangGraph Workflow

The example you'll build in notebook 1 is a tiny two-node RAG pipeline:

```
START → retriever_node → generator_node → END
```

- **`retriever_node`** takes `state["query"]`, scores a small in-memory knowledge base by keyword
  overlap, and returns the top matches as `retrieved_docs` — plus a note appended to `reasoning_steps`.
- **`generator_node`** takes those `retrieved_docs`, builds a prompt, calls the LLM, and returns
  `final_answer` — plus another note appended to `reasoning_steps`.

Wiring it together is four lines:

```python
builder = StateGraph(GraphState)
builder.add_node("retriever_node", retriever_node)
builder.add_node("generator_node", generator_node)
builder.add_edge(START, "retriever_node")
builder.add_edge("retriever_node", "generator_node")
builder.add_edge("generator_node", END)
graph = builder.compile()
```

You'll also call `graph.get_graph().draw_mermaid()` to print a diagram of the graph you just built —
useful any time you want a sanity check that the wiring matches what you intended.

---

## 5️⃣ Debugging Graph Execution

`graph.invoke(initial_state)` only gives you the final state — useful for "did it work," useless for
"what happened in between." For that, use `graph.stream(initial_state)`:

```python
for step_output in graph.stream(initial_state):
    node_name = list(step_output.keys())[0]
    print(node_name, "→", step_output[node_name])
```

Each iteration gives you a dict with exactly one key (the node that just ran) and the update it
returned. This is your main debugging tool for the rest of the course — whenever a graph isn't behaving
the way you expect, stream it before you do anything else.

---

## 6️⃣ LangGraph vs Chains vs AgentExecutor — the full comparison

Notebook 2 walks through all three approaches to the same problem (an agent that can use a calculator
tool and a weather tool) so you feel the differences directly, not just read about them:

| | LCEL Chain | AgentExecutor | LangGraph |
|---|---|---|---|
| Control flow | Fixed sequence (`RunnableBranch` = one fork, no loop-back) | Hidden loop inside the class | Explicit graph — you define every node and edge |
| Adding a new tool | May require restructuring the chain | Add to `tools` list | Add to `tools` list — graph structure unchanged |
| Inspecting intermediate steps | Whatever you print yourself | `return_intermediate_steps=True`, or `verbose=True` logs | `graph.stream(...)` — every node's output, in order |
| Runaway loop protection | N/A | `max_iterations` — silently truncates | `recursion_limit` — raises a catchable `GraphRecursionError` |
| Best for | Strictly linear, no decisions needed | Quick prototypes where you don't need visibility | Anything with branching, looping, multiple agents, or that needs debugging/observability |

The LangGraph version of the agent uses two more pieces worth knowing by name:

- **`ToolNode(tools)`** — a prebuilt node (from `langgraph.prebuilt`) that runs whatever tool calls the
  LLM asked for, so you don't write that loop yourself.
- **`add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})`** — after the
  `agent` node runs, call `should_continue(state)`; whatever string it returns picks the next node.

This `agent ⇄ tools` loop — agent decides, tools execute, back to agent, repeat until no more tool
calls — is the same shape you'll see in every tool-using agent for the rest of the course, including the
multi-agent systems in later weeks.

---

## ✅ Key Takeaways

1. **LangGraph makes the control flow visible.** Chains can't loop; AgentExecutor loops but hides it;
   LangGraph loops *and* shows you every step.
2. **State updates are returned as partial dicts, then merged** — but for lists, that "merge" is a
   replace unless you build the new list yourself (`old + [new]`) or use a reducer like `add_messages`.
3. **`.invoke()` for the final answer, `.stream()` for debugging.** Default to streaming whenever
   something looks wrong.
4. **Conditional edges are how branching/looping works** — a plain function reads the state and returns
   the name of the next node (or `END`).
5. **`recursion_limit` + `GraphRecursionError`** is LangGraph's version of `max_iterations` — but it
   fails loudly and catchably instead of silently truncating.

---

## 🎯 Try It Yourself (both notebooks)

- **Notebook 1:** Add a third node, `critique_node`, that runs after `generator_node`, asks the LLM
  "Does this answer fully address the question? Reply YES or NO," and appends the verdict to
  `reasoning_steps`. You'll need to remove the old `generator_node → END` edge and replace it with
  `generator_node → critique_node → END`.
- **Notebook 2:** Add a third tool (e.g. a `word_counter`, same shape as Week 4's) to the `tools` list
  and re-run the LangGraph version. Notice `should_continue` and the graph wiring never change. Then try
  adding the same tool to the `RunnableBranch` chain from Part A and compare how much code you had to
  touch.

---

## 🔑 Prerequisites

- Python 3.10+
- An **OpenAI API key** in a `.env` file (`OPENAI_API_KEY=...`) in this folder
- Comfort with Week 4's tools/agents content — this week assumes you already know what a `@tool` is and
  roughly how AgentExecutor works, since notebook 2 builds on both

## ⚙️ Setup

```bash
pip install -q langgraph langchain-openai python-dotenv
# Notebook 2 additionally needs:
pip install -q langchain langchain-classic
```

> `langchain-classic` exists because LangChain 1.0 moved `AgentExecutor` and
> `create_tool_calling_agent` out of the main `langchain.agents` module — import them from
> `langchain_classic.agents` instead.

## 🛠️ Troubleshooting

- **`ImportError` for `AgentExecutor` or `create_tool_calling_agent`** — you're importing from
  `langchain.agents`; switch to `langchain_classic.agents`.
- **`reasoning_steps` has fewer entries than expected** — you (or the deliberately-broken example) are
  replacing the list instead of appending to it. Re-read section 3 above.
- **Graph keeps looping forever / hits the recursion limit** — check your conditional edge function;
  make sure there's a real path to returning `END`.
- **`draw_mermaid()` throws an error** — this needs the `grandalf` package in some environments; the
  notebooks already wrap this call in a `try/except` so it won't block you from continuing.

## ☑️ Success Checklist

Before moving on to Week 10, you should be able to:

- [ ] Explain, in your own words, why AgentExecutor's hidden loop becomes a problem at scale
- [ ] Draw (on paper or via `draw_mermaid()`) the graph for a workflow with at least one branch
- [ ] Explain why `state["list_field"] + [new_item]` is needed instead of just returning `[new_item]`
- [ ] Use `graph.stream()` to debug a graph that isn't producing the output you expect
- [ ] Describe the `agent ⇄ tools` loop pattern and what a conditional edge does in it
