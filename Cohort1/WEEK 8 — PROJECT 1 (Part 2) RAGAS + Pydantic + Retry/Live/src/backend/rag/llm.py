from langchain_openai import ChatOpenAI
from src.backend.core.config import settings



def get_llm():
    llm = ChatOpenAI(
    model=settings.OPENAI_MODEL,
    api_key=settings.OPENAI_API_KEY,  # If you prefer to pass api key in directly
    
)
    
    return llm