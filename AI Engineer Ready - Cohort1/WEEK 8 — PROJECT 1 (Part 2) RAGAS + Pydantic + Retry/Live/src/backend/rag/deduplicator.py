from src.backend.logger import GLOBAL_LOGGER as log

def remove_deduplicated_documents(documents):
    """
    Removes duplicate documents from a list based on their content.

    Parameters:
    documents (list): List of document objects, each with a 'page_content' attribute.

    Returns:
    list: A list of document objects with unique content.
    """
    try:
        unique_docs = list({doc.page_content: doc for doc in documents}.values())
        return unique_docs
    except Exception as e:
        log.error("Error during document deduplication", error=str(e))
        raise e