from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """
    Application configuration settings.
    
    Loads configuration from environment variables and .env file.
    Includes settings for model API keys, paths, and LangSmith integration.
    """
    APP_NAME: str = "Multi-Document Assist"
    INDEX_PATH: str ="data/faiss_index"
    DATA_DIR: str = "data/Input_files"

    OPENAI_MODEL: str = Field("", env="OPENAI_MODEL")
    OPENAI_EMBEDDING_MODEL: str = Field("",env="OPENAI_EMBEDDING_MODEL")
    OPENAI_API_KEY: str = Field("", env="OPENAI_API_KEY")
    COHERE_API_KEY: str = Field("", env="COHERE_API_KEY")
    
    LANGSMITH_API_KEY:str = Field("",env="LANGSMITH_API_KEY")
    LANGCHAIN_PROJECT:str = Field("",env = "LANGCHAIN_PROJECT")

    REFERENCE_QUESTION:str = "what is the revenue increase in FY24?"  #Not used in code
    REFERENCE_ANSWER:str = "Revenue increased to USD 120.0 million in FY2024"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
    
settings = Settings()
