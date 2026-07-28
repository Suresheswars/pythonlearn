import requests
import streamlit as st
from src.backend.logger import GLOBAL_LOGGER as log
from src.shared.schemas import QueryRequest, QueryResponse
from typing import Optional


# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------
API_URL = "http://localhost:8000"
REQUEST_TIMEOUT = 300


# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------
def upload_document(file, embedding_model: str):
    try:
        log.info("Uploading document: %s with model: %s", file.name, embedding_model)

        response = requests.post(
            f"{API_URL}/upload",
            files={"file": file},
            data={"embedding_model": embedding_model},
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()
        log.info("Document ingested successfully")
        return response.json().get("chunks", 0)

    except requests.exceptions.Timeout:
        log.error("Upload timed out")
        st.error("⏱️ Upload timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        log.exception("Upload failed")
        st.error(f"❌ Upload failed: {e}")

    return None


def retrieve_answer(question: str, embedding_model: str, retriever_type: str) -> Optional[str]:
    try:
        log.info("Retrieving answer for question: %s with model: %s", question, embedding_model)

        response = requests.post(
            f"{API_URL}/retrieve",
            json={"question": question, "embedding_model": embedding_model, "retriever_type": retriever_type},
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()
        return response.json().get("answer"),response.json().get("answer_texts"),response.json().get("evaluation_metric")

    except requests.exceptions.Timeout:
        log.error("Retrieval timed out")
        st.error("⏱️ Request timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        log.exception("Retrieval failed")
        st.error(f"❌ Failed to retrieve answer: {e}")

    return None