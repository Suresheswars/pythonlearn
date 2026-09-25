"""
WEEK 5 — Live Session: End-to-End RAG Project (Student Copy)

We're building one simple RAG pipeline, live, as a real Python script instead
of a notebook: load PDFs -> chunk -> embed -> store -> retrieve -> generate
answer.

Fill in each function below, in order, following the hints. Run the file
with:

    python rag_project.py

Data files (.env, the 3 policy PDFs) live one folder up, in Live/.
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

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR.parent
PERSIST_DIRECTORY = PROJECT_DIR / "chroma_store"


def load_documents(data_dir):
    """Step 1 — Load the PDFs into LangChain Documents (one per page).

    # Hint: find all *.pdf files in data_dir
    # Hint: use PyPDFLoader(...).load() on each file and collect the results into one list
    # Hint: print the file names found and the total number of pages loaded
    """
    raise NotImplementedError("TODO: load the PDFs from data_dir")


def chunk_documents(docs):
    """Step 2 — Split pages into overlapping chunks.

    # Hint: use RecursiveCharacterTextSplitter with a chunk_size (~1000) and chunk_overlap (~150)
    # Hint: call splitter.split_documents(docs)
    # Hint: print how many chunks were created
    """
    raise NotImplementedError("TODO: split docs into chunks")


def build_vectorstore(chunks, persist_directory):
    """Step 3 — Embed each chunk and store the vectors in Chroma.

    # Hint: create OpenAIEmbeddings(model='text-embedding-3-small')
    # Hint: build the store with Chroma.from_documents(documents=..., embedding=..., persist_directory=str(persist_directory))
    # Hint: Chroma.from_documents ADDS to an existing persist_directory rather than
    #       replacing it - if the folder already exists, delete it first (shutil.rmtree)
    #       so re-running this script doesn't silently double up the store
    # Hint: print how many chunks were embedded
    """
    raise NotImplementedError("TODO: embed chunks and build the vector store")


def get_retriever(vectorstore, k=4):
    """Step 4 — Turn the vector store into a retriever.

    # Hint: vectorstore.as_retriever(search_kwargs={'k': k})
    """
    raise NotImplementedError("TODO: return a retriever from the vector store")


def generate_answer(llm, retriever, question):
    """Step 5 — Retrieve context, then ask the LLM to answer only from it.

    # Hint: retriever.invoke(question) to get the top-k relevant chunks
    # Hint: join the chunks into one context string, including each chunk's source filename
    # Hint: build a SystemMessage that restricts the model to the provided context, and a
    #       HumanMessage with the context + question, asking for citations to source file names
    # Hint: call llm.invoke(messages) and return response.content
    # Hint: before returning, print each retrieved chunk's source + a short preview
    """
    raise NotImplementedError("TODO: retrieve context and generate the answer")


def main():
    """Wire the pipeline together end to end.

    # Hint: load_dotenv(DATA_DIR / '.env', override=True)
    # Hint: call load_documents -> chunk_documents -> build_vectorstore -> get_retriever, in order
    # Hint: create llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)
    # Hint: pick a sample question, call generate_answer(...), and print the final answer
    """
    raise NotImplementedError("TODO: wire the pipeline together")


if __name__ == "__main__":
    main()
