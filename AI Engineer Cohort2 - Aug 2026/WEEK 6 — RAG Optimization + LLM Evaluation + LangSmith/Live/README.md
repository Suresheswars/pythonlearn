# Week 6 (Live) — RAG Optimization + LLM Evaluation + LangSmith

This is the **live-session** material for Week 6. It picks up the working RAG bot built in the
Week 5 Live workbook (`WEEK 5 — RAG Fundamentals (Retrieval-Augmented Generation)/Live/`) and
makes it *reliable*: sharper retrieval, real evaluation scores instead of eyeballing answers, and
full tracing so you can see exactly what the bot is doing.

**Notebooks (run in this order):**

1. [1. WEE6_RAG_Optimization_Live_Session_Student.ipynb](1.%20WEE6_RAG_Optimization_Live_Session_Student.ipynb) — Optimization, Evaluation, LangSmith
2. [2. Langfuse_Basics_Student.ipynb](2.%20Langfuse_Basics_Student.ipynb) — Langfuse (open-source alternative to LangSmith)

> These Live notebooks are a different (more live-coding) pass through the same territory as the
> root-level `01_RAG_Optimization_Student_totry.ipynb` / `02_LangSmith_Demo_Student_totry.ipynb`
> notebooks in the week folder above. Do the Live notebooks in class; the root notebooks are there
> for extra self-paced practice afterward.

---

## Why This Week Matters

A RAG bot that "works" in a demo and a RAG bot a team can trust are not the same thing. This week
closes that gap in three linked parts:

- **Optimize** — fix naive single-query retrieval with a Multi-Query Retriever and Contextual
  Compression, so the bot finds the right chunk even when a user phrases things their own way.
- **Evaluate** — stop eyeballing answers. Score every response on **faithfulness** (is it
  supported by the retrieved context?) and **relevance** (does it actually answer the question?),
  by hand first, then with the standard library (RAGAS / `autoevals`).
- **Observe** — see inside the black box. Trace every retrieval and generation step with
  LangSmith, then do the same thing with Langfuse and compare the two.

---

## What You'll Learn Today

By the end of this session you should be able to:

1. Explain why naive similarity search misses answers, and fix it with Multi-Query Retriever +
   Contextual Compression — without rebuilding the existing retriever.
2. Write hand-rolled faithfulness/relevance LLM-as-judge scorers, and explain why teams reach for
   RAGAS instead of maintaining their own judge prompts forever.
3. Turn on LangSmith tracing with one environment variable, and read a trace to find exactly which
   step (retrieval vs. generation) produced a bad answer.
4. Build a LangSmith dataset + evaluator and use `evaluate()` to compare a baseline vs. an
   optimized retriever run side by side.
5. Explain the LangSmith vs. Langfuse trade-off (managed vs. open-source, cost/latency dashboards)
   well enough to answer it in an interview.
6. Trace a pipeline manually with Langfuse's `@observe` decorator and automatically with its
   LangChain `CallbackHandler`, and nest observations (retriever → generation) inside one trace.
7. Score a Langfuse trace directly (`score_current_trace`) and build a Langfuse dataset/experiment.

---

## Before the Session: Setup

You need three things ready **before** class starts:

### 1. Python environment
Any recent Python 3.10+ environment (venv, conda, or the one from Week 1) works.

### 2. Packages
The notebooks install these for you in the first cells, but you can pre-install to save time:

```bash
pip install -U python-dotenv langchain-community langchain-text-splitters langchain-openai langchain-classic chromadb langsmith
pip install -U langfuse autoevals  # notebook 2 (Langfuse is optional/free-tier)
```

### 3. `.env` file with your API keys
Create a file named `.env` in this same folder (`Live/`) with:

```
OPENAI_API_KEY=sk-your-key-here
LANGSMITH_API_KEY=ls-your-key-here
LANGFUSE_PUBLIC_KEY=pk-your-key-here
LANGFUSE_SECRET_KEY=sk-your-key-here
LANGFUSE_HOST=https://cloud.langfuse.com
```

> ⚠️ Never commit `.env` to Git or share it in chat/Slack. Add it to `.gitignore`.

Get free LangSmith keys at [smith.langchain.com](https://smith.langchain.com) and free Langfuse
keys at [cloud.langfuse.com](https://cloud.langfuse.com) (or self-host Langfuse with Docker).
**Notebook 2 runs top-to-bottom even without Langfuse keys** — `auth_check()` fails gracefully and
every traced call becomes a safe no-op instead of breaking your pipeline.

---

## Notebook 1 — RAG Optimization, Evaluation & LangSmith

| Part | What happens |
|---|---|
| Part 0 — Rebuild the Foundation | Reload the 3 insurance PDFs → chunk → embed → store → base retriever → base answer chain (the Week 5 pipeline), and turn on LangSmith tracing for the whole notebook. |
| Part 1 — Why "It Works" Isn't Enough | Naive single-query retrieval misses rephrased questions → fix with **Multi-Query Retriever** (ask it several ways, merge + de-dupe) and **Contextual Compression** (keep only the relevant lines of each chunk). |
| Part 2 — Measuring What "Good" Means | Hand-roll **faithfulness** and **relevance** LLM-as-judge scorers, then meet **RAGAS**, the maintained library most teams use instead. |
| Part 3 — Seeing Inside the Black Box | LangSmith tracing: automatic (env var, free with LangChain) vs. manual (`@traceable`); datasets, custom evaluators, feedback scoring; comparing baseline vs. optimized runs with `evaluate()`. |
| Part 4 — LangSmith vs. Langfuse | Same job, two companies: managed vs. open-source-first. Sets up notebook 2. |
| Part 5 — Hands-On | Pick your own tricky rephrased question, compare `base_retriever` vs. the optimized retriever, and read the LangSmith trace for both. |

**In-class exercises:** find a real-user-style question that breaks single-query retrieval; run it
through both the base and optimized retrievers; confirm the difference in a LangSmith trace.

---

## Notebook 2 — Langfuse Basics

Mirrors notebook 1's LangSmith section concept-for-concept, so you can translate between the two
tools in an interview without missing a beat.

| Section | What happens |
|---|---|
| Install & Configure | `pip install langfuse`; reads `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` / `LANGFUSE_HOST`; runs safely even when not configured. |
| Trace & Observation | Core concepts — a Trace is one full request, an Observation is one step inside it (`span`, `generation`, `retriever`, `tool`, `chain`, `agent`, `evaluator`, `guardrail`). |
| Tracing an LLM Call | `as_type="generation"` + `update_current_generation(...)` — powers Langfuse's cost/latency dashboards, a strength vs. LangSmith. |
| Automatic Tracing | Pass a `CallbackHandler` into any LangChain `.invoke(...)` — zero decorators, mirrors LangSmith's env-var tracing. |
| Nested Observations | A tiny in-memory-KB RAG pipeline: a `retriever` observation feeding a `generation` observation, nested automatically inside one `chain` trace. |
| Sessions, Users & Tags | Group traces with `session_id` / `user_id` / `tags` via `propagate_attributes`. |
| Scoring | `score_current_trace(...)` attaches faithfulness/relevance scores directly to a trace — feeds Langfuse's quality dashboards. |
| `autoevals` | The maintained, RAGAS-derived scoring library — same idea as RAGAS in notebook 1. |
| Datasets & Experiments | `create_dataset` + `create_dataset_item` (with a gold `expected_output`) — Langfuse's equivalent of LangSmith's Dataset + `evaluate()`. |
| Prompt Management | Langfuse's answer to LangSmith's Prompt Hub — versioned, shared prompts pulled from code. |
| Viewing a Trace & Flushing | `client.flush()` — Langfuse batches traces in the background, so force a flush before checking the UI in a notebook that exits quickly. |

**In-class exercise:** trace the same nested RAG example manually with `@observe`, then again with
the automatic `CallbackHandler`, and compare what shows up in the Langfuse UI.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `OPENAI_API_KEY` / `LANGSMITH_API_KEY` not found | `.env` missing, misnamed, or not in this folder | Create `.env` next to the notebook, no quotes around the key, then re-run the setup cell |
| No trace appears in LangSmith | `LANGSMITH_TRACING` / `LANGCHAIN_TRACING_V2` not set to `'true'`, or wrong `LANGCHAIN_PROJECT` | Re-run the Part 0 setup cell and check the project name in the LangSmith UI |
| Langfuse cells run but nothing shows in the UI | `AUTH_OK` is `False` (keys missing/invalid) | Expected — the notebook still runs; add real keys to `.env` to see live traces |
| Nothing shows up until you check the UI | Langfuse batches traces in the background | Call `client.flush()` before switching to the browser |
| `ModuleNotFoundError` (e.g. `langchain_classic`, `chromadb`, `langfuse`) | Packages not installed in the active kernel | Re-run the pip install cell, then **restart the kernel** |
| Optimized retriever isn't actually better | Multi-query LLM call failed silently, or compression stripped the answer sentence | Print the raw retrieved chunks before and after each step to isolate where it breaks |

**The 4-step debugging process (same as previous weeks):**
1. Identify where it breaks (retrieval? compression? judge scoring? tracing?)
2. Print intermediate outputs (retrieved chunks, judge scores, `auth_check()` result)
3. Check assumptions (right `.env` keys? tracing env vars set *before* the chain runs?)
4. Read the trace itself — that's the entire point of this week's tooling

---

## Quick Glossary (also in the notebooks)

- **Multi-Query Retriever** — ask the same question several ways, search each, merge + de-dupe
- **Contextual Compression** — keep only the relevant lines of each retrieved chunk
- **Faithfulness** — is the answer supported by the retrieved context (no hallucination)?
- **Relevance** — does the answer actually address what was asked?
- **LLM-as-a-Judge** — a strong LLM grades another model's answer against a rubric
- **RAGAS** — the standard maintained library for RAG evaluation metrics
- **Trace** — one full request, start to finish (LangSmith and Langfuse both use this term)
- **Observation** — one step inside a Langfuse trace (`span`, `generation`, `retriever`, ...)
- **`@traceable` / `@observe`** — manual tracing decorators (LangSmith / Langfuse)
- **`autoevals`** — Langfuse-side, RAGAS-derived scoring library

---

## What to Submit

1. Both completed Live notebooks, run top-to-bottom.
2. In a markdown cell at the bottom (or on the LMS), answer:
   - One optimization that improved retrieval quality most
   - One evaluation signal you trusted most
   - One difference you noticed between LangSmith and Langfuse

## Success Checklist

- [ ] `.env` loads and the setup cell confirms `OPENAI_API_KEY` / `LANGSMITH_API_KEY` are present
- [ ] Notebook 1: optimized retriever (multi-query + compression) visibly outperforms the base retriever on a rephrased question
- [ ] Notebook 1: at least one hand-rolled faithfulness/relevance score computed and explained
- [ ] Notebook 1: a LangSmith trace inspected for at least one query
- [ ] Notebook 2: `auth_check()` result printed and understood (works with or without real keys)
- [ ] Notebook 2: nested trace (retriever → generation) built and viewed
- [ ] Reflection questions answered
