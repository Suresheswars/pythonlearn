"""
WEEK 5 — Live Session: End-to-End RAG Project (Master / Instructor Copy)

We build one simple RAG pipeline, live, as a real Python script instead of a
notebook: load PDFs -> chunk -> embed -> store -> retrieve -> generate answer.

Speaker notes are written as comments right above the code they explain, so
you can teach straight from this file. Run it with:

    python rag_project.py

Data files (.env, the 3 policy PDFs) live one folder up, in Live/, so both
the master and student projects can share them without duplicating anything.
"""

import shutil
import sys
from pathlib import Path

# PDFs sometimes contain glyphs (bullets, smart quotes, ligatures) that
# Windows' default console codepage (cp1252) can't print. Switch stdout to
# UTF-8 so a print() never crashes the pipeline over a display character.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Everything reads/writes relative to this folder, and looks one level up
# (Live/) for the shared .env and the source PDFs.
PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR.parent
PERSIST_DIRECTORY = PROJECT_DIR / "chroma_store"


def load_documents(data_dir):
    """Step 1 — Load the PDFs into LangChain Documents (one per page).

    Speaker notes:
    - Point students at the 3 PDFs in Live/ and show the file names before loading.
    - Each page becomes one Document with `page_content` + `metadata['source']`.
    - This is the "raw text enters the pipeline" moment — show a preview after loading.
    """
    pdf_files = sorted(data_dir.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in {data_dir}")

    docs = []
    for pdf_file in pdf_files:
        docs.extend(PyPDFLoader(str(pdf_file)).load())

    print("PDF files:", [p.name for p in pdf_files])
    print("Loaded pages:", len(docs))
    return docs


def chunk_documents(docs):
    """Step 2 — Split pages into overlapping chunks.

    Speaker notes:
    - chunk_size controls how much text goes into one embedding.
    - chunk_overlap keeps context from being lost right at a chunk boundary.
    - RecursiveCharacterTextSplitter tries paragraph -> line -> word splits, in
      that order, so it breaks on the most natural boundary it can find.
    - Live tweak: change chunk_size to 400 or 1500 and re-run to show the
      chunk count and preview change.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(docs)

    print("Chunks created:", len(chunks))
    return chunks


def build_vectorstore(chunks, persist_directory):
    """Step 3 — Embed each chunk and store the vectors in Chroma.

    Speaker notes:
    - text-embedding-3-small is a strong, cheap default for a classroom demo.
    - persist_directory writes the vectors to disk so the store survives a
      kernel/process restart — worth pointing out since it's a common gotcha.
    - Chroma.from_documents *adds* to an existing persist_directory instead of
      replacing it, so re-running this script would silently double up the
      store (and go stale the moment chunk_size changes). We wipe any old
      store first so every run starts from a clean, correct index — call
      this out live, it's a real gotcha people hit in production too.
    """
    if persist_directory.exists():
        shutil.rmtree(persist_directory)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(persist_directory),
    )

    print("Vector store ready:", len(chunks), "chunks embedded")
    return vectorstore


def get_retriever(vectorstore, k=4):
    """Step 4 — Turn the vector store into a retriever.

    Speaker notes:
    - k is how many chunks come back per question. Show k=3 vs k=6 live and
      discuss the precision/recall trade-off (too few chunks -> missed
      context; too many -> noisy, expensive prompts).
    """
    return vectorstore.as_retriever(search_kwargs={"k": k})


def generate_answer(llm, retriever, question):
    """Step 5 — Retrieve context, then ask the LLM to answer only from it.

    Speaker notes:
    - This is the full RAG loop in one function: Retrieve -> Augment (build
      the context string) -> Generate.
    - The system prompt explicitly restricts the model to the provided
      context — this is what keeps the demo grounded instead of the model
      answering from its own general knowledge.
    - Print the retrieved chunk sources before the answer so students see
      *why* the model said what it said.
    """
    context_docs = retriever.invoke(question)
    context_text = "\n\n".join(
        f"Source: {doc.metadata.get('source', 'unknown')}\n{doc.page_content}"
        for doc in context_docs
    )

    messages = [
        SystemMessage(
            content=(
                "You are a helpful tutor. Answer only from the provided context "
                "and keep the answer clear and student-friendly."
            )
        ),
        HumanMessage(
            content=(
                f"Context:\n{context_text}\n\nQuestion: {question}\n\n"
                "Answer with short citations to the source file names."
            )
        ),
    ]

    print("Retrieved context preview:")
    for doc in context_docs:
        source_name = doc.metadata.get("source", "unknown")
        preview = doc.page_content[:200].replace("\n", " ")
        print("-", source_name)
        print(" ", preview + ("..." if len(doc.page_content) > 200 else ""))

    response = llm.invoke(messages)
    return response.content


def main():
    """Wire the pipeline together end to end.

    Speaker notes:
    - This is the moment to say "this is now a real script, not a notebook —
      anyone on your team could run this file."
    - After this runs once, show students how to swap the question, k, or
      chunk_size and re-run just main() without re-reading/re-chunking the
      PDFs (that's the natural lead-in to "why we'd want a project structure
      with separate steps instead of one long notebook cell").
    """
    load_dotenv(DATA_DIR / ".env", override=True)

    docs = load_documents(DATA_DIR)
    chunks = chunk_documents(docs)
    vectorstore = build_vectorstore(chunks, PERSIST_DIRECTORY)
    retriever = get_retriever(vectorstore, k=4)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    question = "What benefits are described in the documents?"
    print("\nQuestion:", question)
    answer = generate_answer(llm, retriever, question)

    print("\nFinal answer:")
    print(answer)


if __name__ == "__main__":
    main()
