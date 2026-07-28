# ============================================================================
# 1_website_knowledge_server_student.py -- the capstone MCP server.
# Owns two tools that together form the whole pipeline:
#   learn_website(url)  -- crawl -> chunk -> embed -> store   (Sections 2 & 3)
#   ask_question(query) -- retrieve -> generate               (Section 4)
# Build it yourself using the hints below.
# ============================================================================

# TODO: import os, sys
# hint: os.environ.setdefault("USER_AGENT", "Week12-Capstone-Bot/1.0") BEFORE importing
# WebBaseLoader -- without a UA, LangChain warns on every crawl and some sites
# reject the blank default user agent

# TODO: from dotenv import load_dotenv, find_dotenv
# TODO: from mcp.server.fastmcp import FastMCP
# TODO: from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# TODO: from langchain_chroma import Chroma
# (note: langchain_community.vectorstores.Chroma also works but is deprecated --
# use the langchain_chroma package instead)
# TODO: from langchain_community.document_loaders import WebBaseLoader
# TODO: from langchain_text_splitters import RecursiveCharacterTextSplitter
# TODO: from langchain_core.prompts import ChatPromptTemplate
# TODO: from langchain_core.output_parsers import StrOutputParser
# TODO: from langchain_core.runnables import RunnablePassthrough

# TODO: load_dotenv(find_dotenv())

# TODO: fail fast if OPENAI_API_KEY is missing -- print a clear error to stderr
# and sys.exit(1) here, instead of letting the first tool call crash confusingly
# mid-class inside OpenAIEmbeddings

# TODO: create the server -- FastMCP("WebsiteKnowledgeServer", host="127.0.0.1", port=8010)


# ----------------------------------------------------------------------------
# The state: one persistent Chroma collection, shared by both tools below.
# This is Section 3 ("Adding State with ChromaDB") made concrete -- every
# learn_website() call should ADD to this same collection, not replace it.
# ----------------------------------------------------------------------------

# TODO: embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
# TODO: create a Chroma vector_store with collection_name="website_knowledge",
# embedding_function=embeddings, persist_directory=<path next to this file>
# hint: os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_website_knowledge")
# -- NOT a relative "./chroma_website_knowledge": if Claude Desktop (Section 5)
# ever launches this script, its working directory won't be this folder, so a
# relative path resolves to the wrong place and Chroma fails with a permissions
# error trying to create it there
# TODO: retriever = vector_store.as_retriever(search_kwargs={"k": 4})
# TODO: llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# TODO: write ANSWER_TEMPLATE, a prompt string with {context} and {question}
# placeholders that instructs the LLM to answer ONLY from the given context
# and to say "I don't know" when the context doesn't contain the answer


# TODO: write learn_website(url: str) -> str, decorated with @mcp.tool()
# hint: strip() the url and check it starts with "http://" or "https://" --
# return a clear message instead of crawling garbage if it doesn't
# hint: loader = WebBaseLoader(url, requests_kwargs={"timeout": 15}, raise_for_status=True)
# -- the timeout stops one slow/unresponsive site from hanging the whole call,
# and raise_for_status makes a 404/500 fail loudly instead of "learning" an
# error page as if it were real content
# hint: docs = loader.load()
# hint: split docs with RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# hint: filter out any chunks with empty/whitespace-only page_content before storing
# hint: vector_store.add_documents(chunks) -- this is what makes the knowledge
# base grow across multiple calls instead of resetting each time
# hint: wrap in try/except and return a clear message either way
# hint: write a docstring an LLM could read to know exactly when to call this
# (e.g. "learn https://example.com" or "read this page")


# TODO: write ask_question(query: str) -> str, decorated with @mcp.tool()
# hint: build a ChatPromptTemplate.from_template(ANSWER_TEMPLATE)
# hint: chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser()
# hint: return chain.invoke(query)
# hint: write a docstring an LLM could read to know exactly when to call this


# ============================================================================
# TWO WAYS TO RUN THIS SERVER
# hint: Option A - mcp.run(transport="stdio") -- for Claude Desktop (Section 5),
# which launches this script itself and talks over stdin/stdout
# hint: Option B - mcp.run(transport="sse") -- what we use live in class so
# our own 2_rag_client_student.py can connect to it over the network
# ============================================================================

# TODO: under if __name__ == "__main__": call mcp.run(transport="sse")

# MCP Inspector -> Debugging & Development env


# Website URL -> learn_website() -> Load Website -> Split it in to Chunks -> Create Embeddings -> Store in Chroma -> ask_question() -> Retrieve relevent chunks -> LLM -> Answer to the end user

import os
import sys

from dotenv import load_dotenv, find_dotenv
from mcp.server.fastmcp import FastMCP
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv(find_dotenv())

os.getenv("OPENAI_API_KEY")

mcp = FastMCP("WebsiteKnowledgeServer", host = "127.0.0.1", port = 8010)

# Embeddings:
embeddings = OpenAIEmbeddings(model = "text-embedding-3-small")

# Persist Directory:
PERSIST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_website_knowledge")

vector_store = Chroma(
    collection_name = "website_knowledge",
    embedding_function = embeddings,
    persist_directory = PERSIST_DIR
)

retriever = vector_store.as_retriever(search_kwargs = {"k": 4})

llm = ChatOpenAI(model = "gpt-4o-mini", temperature = 0)

ANSWER_TEMPLATE = """You are a helpful assistant that ONLY answers questions based on the provided context.

STRICT RULES:
1. ONLY use information from the context below.
2. Do NOT use your general knowledge or training data.
3. If the context doesn't contain the answer, respond with: "I don't know - this information wasn't found in the learned websites."
4. Mention which website the answer came from when you can.

Context from learned websites:
{context}

Question: {question}

Answer (based ONLY on the context above):"""

@mcp.tool()
def learn_website(url: str) -> str:
    """Crawl a website URL and add its content to the knowledge base.
    
        Use this whenever the user gives you a URL and asks you to learn, read,
        ingest, or remember it. Safe to call multiple times with different URLs --
        each call adds to the same knowledge base, it does not replace it.
    
        Args:
            url: the full URL of the website to crawl, e.g. "https://example.com/docs"
    """

    url.strip()
    if not url.startswith(("http://", "https://")):
        return f'"{url}" is not a valid URL -- it must start with http:// or https://.'
    try:
        loader = WebBaseLoader(url, requests_kwargs = {"timeout": 15}, raise_for_status = True)
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
        chunks = splitter.split_documents(docs)
        chunks = [c for c in chunks if c.page_content.strip()]
        if not chunks:
            return f"Loaded {url} but found no usable text content -- nothing was added."
        vector_store.add_documents(chunks)
        return f"Learned {url} -- added {len(chunks)} chunks to the knowledge base."
    except Exception as e:
        return f"Error learning {url}: {e}"

@mcp.tool()
def ask_question(query: str) -> str:
    """Answer a question using only the websites learned so far via learn_website.
    
        Use this whenever the user asks a question that should be answered from
        previously-learned website content. If nothing relevant was learned yet,
        says so instead of guessing from general knowledge.
    
        Args:
            query: the natural-language question to answer
    """
    prompt = ChatPromptTemplate.from_template(ANSWER_TEMPLATE)
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain.invoke(query)

# stdio/ stdout -> Standard Input/ Standard Output

mcp.run(transport = "stdio")
# Claude Desktop -> website_server.py -> stdin/ stdout pipes -> Tools -> The server is never exposed on a port; -> alter the config file 
# if __name__ == "__main__":
#     mcp.run(transport = "sse")
