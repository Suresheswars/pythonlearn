# from langchain_huggingface import HuggingFaceEmbeddings

# def get_embeddings():
#     embeddings = HuggingFaceEmbeddings(
#                 model_name="sentence-transformers/all-MiniLM-L6-v2"
#             )
    
#     return embeddings


from langchain_openai import OpenAIEmbeddings
from langchain_cohere import CohereEmbeddings
from src.backend.core.config import settings

def get_embeddings(model_type: str):
    
    if model_type == "OpenAI (text-embedding-3-large)":
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large",
            api_key=settings.OPENAI_API_KEY
        )
    elif model_type == "Cohere (embed-english-v3.0)":
        embeddings = CohereEmbeddings(
            cohere_api_key=settings.COHERE_API_KEY,
            model="embed-english-v3.0" 
        )
    elif model_type == "OpenAI (text-embedding-3-small)":
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=settings.OPENAI_API_KEY
        )

    return embeddings
