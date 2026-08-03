from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_classic.retrievers import MultiQueryRetriever
from src.backend.logger import GLOBAL_LOGGER as log
from src.backend.rag.llm import get_llm
from src.backend.core.config import settings

def multi_query_retrieval(index_path, query: str, embeddings):

    try:

        log.info('Multi Query Retriever Invoked')

        llm = get_llm()

        # Load FAISS index
        new_db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        log.info('FAISS index loaded')

        new_db_retriever = new_db.as_retriever(search_kwargs={"k": 3})

        # Define a custom prompt template
        custom_prompt = PromptTemplate(
            input_variables=["question"],
            template="Generate 3 different versions of this question: {question}"
        )

        # Initialize MultiQueryRetriever with custom prompt
        multi_query_retriever_custom = MultiQueryRetriever.from_llm(
            retriever=new_db_retriever,
            llm= llm,
            prompt=custom_prompt,
            include_original=False  # Exclude the original query
        )

        # Use the custom retriever to fetch documents
        relevant_docs = multi_query_retriever_custom.invoke(query)

        log.info('Multi Query Retriever Docs fetched', docs=relevant_docs)

        return relevant_docs

    except Exception as e:
        log.error("Error during Multi Query Retrieval", error=str(e))
        raise e