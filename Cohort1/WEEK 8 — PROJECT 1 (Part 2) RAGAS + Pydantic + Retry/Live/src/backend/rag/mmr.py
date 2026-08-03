from langchain_community.vectorstores import FAISS
from src.backend.rag.embeddings import get_embeddings
from src.backend.logger import GLOBAL_LOGGER as log
from src.backend.core.config import settings
def mmr(index_path, query: str, embeddings):
    try:
        log.info("MMR invoked", query=query)


        # Load FAISS index
        new_db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        log.info('FAISS index loaded')

        

        docs = new_db.max_marginal_relevance_search(
            query=query,
            k=5, #Number of embeddings to select out of fetch_k
            fetch_k=20,
            lambda_mult=0.7 # (0 to 0.5 - Supports Diversity, 0.5 to 1 - Supports Relevancy )
        )

        log.info("MMR documents retrieved", count=len(docs))

        return docs

    except Exception as e:
        log.error("Error during MMR retrieval", error=str(e))
        raise e