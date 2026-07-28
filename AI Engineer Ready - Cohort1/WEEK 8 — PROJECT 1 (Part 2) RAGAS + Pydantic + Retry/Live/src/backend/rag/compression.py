from src.backend.logger import GLOBAL_LOGGER as log
from src.backend.rag.llm import get_llm
from langchain_community.vectorstores import FAISS
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_cohere.rerank import CohereRerank
from src.backend.core.config import settings

def contextual_compression(index_path,query,embeddings):
    try:
        log.info("Contextual compression invoked", query=query)


        new_db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True).as_retriever()
        log.info('FAISS index loaded')

        compressor=CohereRerank(model="rerank-v3.5",cohere_api_key=settings.COHERE_API_KEY)

        ## here re ranker is used so first base retriever will give information and compressor will try compress the chunks and rerank as per the query relevnacy
        compression_retriever=ContextualCompressionRetriever(base_compressor=compressor,base_retriever=new_db)
        compressed_docs = compression_retriever.invoke(query)
        
        log.info('Compression Retriever fetched documents')
        return compressed_docs

    except Exception as e:
        log.error("Error during contextual compression", error=str(e))
        raise e