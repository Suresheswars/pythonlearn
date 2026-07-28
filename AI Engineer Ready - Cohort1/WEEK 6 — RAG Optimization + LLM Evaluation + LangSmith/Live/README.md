# WEEK 6 - RAG Optimization Live Session

This folder contains the student notebook for the live session on RAG optimization, LLM evaluation, and LangSmith tracing.

## Contents

- `1. WEE6_RAG_Optimization_Live_Session_Student.ipynb`

## What the notebook covers

The notebook walks through an end-to-end RAG workflow:

1. Checking the local environment and required API keys.
2. Loading the PDF source documents from the current folder.
3. Chunking the documents for retrieval.
4. Creating embeddings and a Chroma vector store.
5. Retrieving the most relevant chunks for a question.
6. Generating answers with an OpenAI chat model.
7. Comparing retrieval behavior across sample questions.

It also includes short markdown notes after code cells so students can follow the purpose of each step.

## Requirements

The notebook expects:

- Python 3.10+.
- A `.env` file in this folder or the necessary environment variables set another way.
- `OPENAI_API_KEY` for embeddings and chat completion.
- `LANGSMITH_API_KEY` if you want LangSmith tracing.
- Three PDF files in the same folder as the notebook.

## Suggested packages

Install the notebook dependencies with:

```bash
pip install python-dotenv langchain-community langchain-text-splitters langchain-openai chromadb pypdf
```

## How to run

1. Place the required PDF files in this folder.
2. Set your API keys in `.env` or the shell.
3. Open the notebook in VS Code or Jupyter.
4. Run the cells from top to bottom.

## Notes

- The notebook uses `Chroma` with a local persistence directory named `rag_chroma_store`.
- If retrieval looks weak, try changing chunk size, chunk overlap, or the `k` value used by the retriever.
- The notebook is designed as a teaching demo, so the code is intentionally direct and easy to read.