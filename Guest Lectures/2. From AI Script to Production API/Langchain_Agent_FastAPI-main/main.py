#FastAPI application entry point
# This ties everything together. It initializes FastAPI and mounts the controllers (routers).

from fastapi import FastAPI
from controllers.agent_cotroller import router as agent_router
from system.config import settings

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="A cleanly structured API demonstrating LangChain integration.",
    version="1.0.0"
)

# Include the controllers (routers)
app.include_router(agent_router)

@app.get("/", tags=["Health Check"])
def root():
    return {"status": "online", "message": f"Welcome to {settings.app_name}"}

# To run the server:
# uvicorn main:app --reload