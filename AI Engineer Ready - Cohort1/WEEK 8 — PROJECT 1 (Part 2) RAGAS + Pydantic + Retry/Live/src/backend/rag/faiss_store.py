from langchain_community.vectorstores import FAISS
from src.backend.logger import GLOBAL_LOGGER as log
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from src.backend.rag.embeddings import get_embeddings
from src.backend.core.config import settings

def index_docs(chunks, embedding_model: str): #Index the documents to FAISS Vector Store
    
    # Guard: Skip if no chunks to index
    if not chunks or len(chunks) == 0:
        log.warning("No chunks to index", embedding_model=embedding_model)
        return
    
    embeddings = get_embeddings(embedding_model)
    # create a dynamic path based on the embedding model so they don't overwrite each other
    index_path = f"{settings.INDEX_PATH}_{embedding_model}"

    try:
        vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        log.info("Loading existing FAISS index")
        new_texts = [doc.page_content for doc in chunks]
        vector_store.add_texts(new_texts)
        vector_store.save_local(index_path)
        log.info("FAISS index updated and saved", index_path=index_path)
    
    except Exception as e:
        
        log.info(f"FAISS index not found for {embedding_model}, Creating a new FAISS index")

        # Create sample embedding to get dimension
        sample_embedding = embeddings.embed_query('hello')
        index = faiss.IndexFlatL2(len(sample_embedding))

        vector_store = FAISS(
            embedding_function=embeddings,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={}
        )

        vector_store.add_documents(documents=chunks)
        vector_store.save_local(index_path)
        log.info("FAISS index created and saved at ", index_path= index_path)