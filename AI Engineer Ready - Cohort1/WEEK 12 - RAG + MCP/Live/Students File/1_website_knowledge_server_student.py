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
# embedding_function=embeddings, persist_directory="./chroma_website_knowledge"
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
