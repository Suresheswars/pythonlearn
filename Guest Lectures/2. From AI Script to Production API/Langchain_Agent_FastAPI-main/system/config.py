# Environment variables and system setup
# This file handles the system-level configuration, loading environment variables like API keys so they aren't hardcoded.

import os
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = "LangChain Agent Showcase"
    openai_api_key: str = Field("", env = "OPENAI_APIKEY")
    
    class Config:
        env_file = ".env"

# Instantiate settings to be used across the app
settings = Settings()