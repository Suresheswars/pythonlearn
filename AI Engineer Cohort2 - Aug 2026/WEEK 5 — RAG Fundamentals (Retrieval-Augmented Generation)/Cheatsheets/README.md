# Week 5 Cheatsheets

Printable quick-reference PDFs covering the six learning outcomes from the Week 5 README: why RAG beats direct prompting, document loading & preprocessing, chunking strategies, embeddings & vector stores, retriever + LLM chains, and evaluating RAG quality. Each sheet also ends with an **Interview Prep** section of likely interview Q&amp;A for that topic.

| # | Cheatsheet | Covers |
|---|---|---|
| 1 | [Why RAG? Cheatsheet](01_Why_RAG_Cheatsheet.pdf) | What RAG is, why direct prompting hallucinates/goes stale, the six-stage RAG pipeline, RAG vs fine-tuning vs prompting, when to reach for RAG. |
| 2 | [Document Loading & Preprocessing](02_Document_Loading_Preprocessing_Cheatsheet.pdf) | Loaders (TextLoader, PyPDFLoader, DirectoryLoader, CSV/Unstructured), preprocessing steps, keeping metadata alive for citations, scanned-PDF/OCR pitfall. |
| 3 | [Chunking Strategies Cheatsheet](03_Chunking_Strategies_Cheatsheet.pdf) | Fixed-size vs recursive vs token-based vs semantic vs structure-aware splitting, chunk size/overlap guidance, how to choose per document type. |
| 4 | [Embeddings & Vector Stores](04_Embeddings_Vector_Stores_Cheatsheet.pdf) | Embedding models (OpenAI, sentence-transformers, Cohere), vector stores (FAISS, Chroma, Pinecone), similarity metrics, code example. |
| 5 | [Retriever + LLM Chain Cheatsheet](05_Retriever_LLM_Chain_Cheatsheet.pdf) | Retriever types (similarity, MMR, threshold, hybrid), building a RetrievalQA chain, grounded-answer prompt template. |
| 6 | [Evaluating RAG Quality](06_Evaluating_RAG_Quality_Cheatsheet.pdf) | Retrieval metrics (precision@k, recall@k, MRR), generation metrics (faithfulness, relevancy), tools (RAGAS, LangSmith), manual eval checklist. |

## When to reach for which one

- Explaining why a plain chatbot isn't enough for factual/internal-doc questions? → **01**
- Getting text out of a messy PDF or folder of documents? → **02**
- Deciding how to split a document before embedding it? → **03**
- Choosing an embedding model or vector database? → **04**
- Wiring retrieval into an actual LLM answer chain? → **05**
- Answers look plausible but you're not sure if they're trustworthy? → **06**
