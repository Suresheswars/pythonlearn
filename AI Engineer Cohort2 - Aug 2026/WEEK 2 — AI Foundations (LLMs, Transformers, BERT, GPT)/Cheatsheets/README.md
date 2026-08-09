# Week 2 Cheatsheets

Printable quick-reference PDFs covering the six learning outcomes from the Week 2 README: language models, tokenization, embeddings, transformers/attention, BERT vs GPT, and LLM limitations.

| # | Cheatsheet | Covers |
|---|---|---|
| 1 | [Language Models Cheatsheet](01_Language_Models_Cheatsheet.pdf) | Next-token prediction, where LMs show up, evolution from n-grams to transformers, key terms (LLM, autoregressive, parameters, context window). |
| 2 | [Tokenization & Vocabulary Cheatsheet](02_Tokenization_Vocabulary_Cheatsheet.pdf) | Token vs tokenization vs vocabulary, why it matters for cost/context, tokenization differences across models, counting tokens with `tiktoken`. |
| 3 | [Embeddings & Vector Space Cheatsheet](03_Embeddings_Vector_Space_Cheatsheet.pdf) | What embeddings are, use cases, choosing an embedding model, cosine similarity, generating embeddings via the OpenAI API. |
| 4 | [Transformer & Attention Cheatsheet](04_Transformer_Attention_Cheatsheet.pdf) | Transformer core blocks, attention intuition, Query/Key/Value, the attention formula, encoder vs decoder vs seq2seq decision rule. |
| 5 | [BERT vs GPT Cheatsheet](05_BERT_vs_GPT_Cheatsheet.pdf) | Encoder-only vs decoder-only side-by-side, masked language modeling, context sensitivity, GPT decoding settings (temperature). |
| 6 | [LLM Limitations Quick-Reference Card](06_LLM_Limitations_Quick_Reference.pdf) | Hallucinations, knowledge cutoff, prompt sensitivity, bias, context limits — one-page symptom → cause → fix table, plus a session wrap-up checklist. |

## When to reach for which one

- Explaining what an LLM actually does under the hood? → **01**
- Estimating cost or debugging a context-length error? → **02**
- Building semantic search or a RAG retriever? → **03**
- Explaining how attention/transformers work? → **04**
- Deciding whether a task needs an encoder or a decoder model? → **05**
- Something the model said sounds off? → **06** first — it's the fastest lookup.
