import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from src.backend.logger import GLOBAL_LOGGER as log


def _load_single_file(file_path):
    if os.path.getsize(file_path) == 0:
        log.warning("Skipping empty file", file_path=file_path)
        return []

    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
        return loader.load()
    if file_path.endswith(".docx"):
        loader = Docx2txtLoader(file_path)
        return loader.load()
    if file_path.endswith(".txt"):
        loader = TextLoader(file_path, encoding="utf-8")
        return loader.load()

    log.warning("Skipping unsupported file type", file_path=file_path)
    return []


def load_document(directory_path):
    try:
        documents = []
        if os.path.isfile(directory_path):
            return _load_single_file(directory_path)

        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            documents.extend(_load_single_file(file_path))

        return documents
    except Exception as e:
        log.error("Error loading documents from directory", error=str(e), directory=directory_path)
        raise e