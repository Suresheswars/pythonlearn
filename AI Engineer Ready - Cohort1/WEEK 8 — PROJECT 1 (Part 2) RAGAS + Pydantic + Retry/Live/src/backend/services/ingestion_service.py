import os
from fastapi import UploadFile
from src.backend.rag.loader import load_document
from src.backend.rag.splitter import split_documents
from src.backend.rag.faiss_store import index_docs
from src.backend.logger import GLOBAL_LOGGER as log
from tenacity import retry, stop_after_attempt, wait_exponential
from src.backend.core.config import settings
from langsmith import traceable



@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True
)
@traceable(run_type="chain", name="Ingest Document", project_name=settings.LANGCHAIN_PROJECT)
async def ingest_document(file: UploadFile, embedding_model: str) -> int:
    """
    Ingests a document file, splits it into chunks, and indexes it.

    Args:
        file (UploadFile): The file to be ingested.
        embedding_model (str): The name of the embedding model to use.

    Returns:
        int: The number of chunks created and indexed.

    Raises:
        Exception: If any error occurs during ingestion.
    """

    try:
        os.makedirs(settings.DATA_DIR, exist_ok=True)

        file_path = os.path.join(settings.DATA_DIR, file.filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        log.info("File saved", file=file.filename)

        docs = load_document(file_path)
        chunks = split_documents(docs)

        index_docs(chunks, embedding_model)

        log.info("Documents indexed", chunks=len(chunks))
        return len(chunks)
    
    except Exception as e:
        log.error("Error during Ingestion service", error=str(e))
        raise e
