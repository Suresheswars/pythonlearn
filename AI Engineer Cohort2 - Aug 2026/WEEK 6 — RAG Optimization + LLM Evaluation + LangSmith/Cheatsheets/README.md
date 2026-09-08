# Week 6 Cheatsheets

Printable quick-reference PDFs covering the Week 6 live session: sharper retrieval (Multi-Query + Contextual Compression), RAG evaluation metrics (Faithfulness & Relevance), LLM-as-a-Judge, evaluation libraries (RAGAS vs DeepEval), and LLM observability (LangSmith core concepts + LangSmith vs Langfuse). Each sheet also ends with an **Interview Prep** section of likely interview Q&amp;A for that topic.

| # | Cheatsheet | Covers |
|---|---|---|
| 1 | [Sharper Retrieval Cheatsheet](01_Sharper_Retrieval_Cheatsheet.pdf) | Why naive similarity search breaks, Multi-Query Retriever (ask it more ways), Contextual Compression (read only what matters), when to use each, LangChain code for both. |
| 2 | [RAG Evaluation Metrics Cheatsheet](02_RAG_Evaluation_Metrics_Cheatsheet.pdf) | Why evaluation matters at scale, Faithfulness vs Relevance definitions, reading both scores together, how a combined score gets produced. |
| 3 | [LLM-as-a-Judge Cheatsheet](03_LLM_as_a_Judge_Cheatsheet.pdf) | What an LLM judge is, pairwise vs absolute scoring, a minimal judge prompt, known judge biases (verbosity, position, self-preference), best practices. |
| 4 | [RAGAS vs. DeepEval Cheatsheet](04_RAGAS_vs_DeepEval_Cheatsheet.pdf) | Why use a maintained library instead of hand-rolling, RAGAS and DeepEval overviews with code, head-to-head comparison, rule-of-thumb decision guide. |
| 5 | [LangSmith Core Concepts Cheatsheet](05_LangSmith_Core_Concepts_Cheatsheet.pdf) | What LLM observability is, Project → Trace → Run, automatic vs `@traceable` tracing, Datasets/Evaluators/Feedback, Compare Runs & Prompt Hub. |
| 6 | [LangSmith vs. Langfuse Cheatsheet](06_LangSmith_vs_Langfuse_Cheatsheet.pdf) | What Langfuse is, head-to-head comparison with LangSmith, self-hosting/data-residency angle, quick setup code for both. |

## When to reach for which one

- Your bot misses answers you know are in the document? → **01**
- Need to prove an answer is grounded and on-topic, not just "looks fine"? → **02**
- Scoring thousands of answers without a human reading every one? → **03**
- Deciding between hand-rolling metrics or picking an evaluation library? → **04**
- Debugging why a chain gave a bad answer, step by step? → **05**
- Choosing which observability tool to adopt for a real project? → **06**
