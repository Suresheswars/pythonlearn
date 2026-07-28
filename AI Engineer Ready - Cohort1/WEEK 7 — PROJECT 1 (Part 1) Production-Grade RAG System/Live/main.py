import os
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.backend.core.config import settings
from langsmith import traceable

# Setup Environment Variables (MUST BE BEFORE OTHER IMPORTS)
# LangSmith and system configuration
os.environ["KMP_DUPLICATE_LIB_OK"] = "True"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGSMITH_API_KEY"] = settings.LANGSMITH_API_KEY
os.environ["LANGCHAIN_PROJECT"] = settings.LANGCHAIN_PROJECT

from src.backend.api import routes,health
from src.backend.logger import GLOBAL_LOGGER as log

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    log.info(
        "Request processed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration=f"{process_time:.4f}s"
    )
    
    return response


app.include_router(routes.router)
app.include_router(health.router)

@traceable()
@app.get("/")
def root():
    return {"message": "Multi-Document-Assist API"}