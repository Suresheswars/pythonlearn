from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.backend.logger import GLOBAL_LOGGER as log


def split_documents(documents):
    
    log.info('Splitting Documents')
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=50)
    split_docs = text_splitter.split_documents(documents)
    
    return split_docs
