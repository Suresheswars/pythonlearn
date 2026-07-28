# API Routing and HTTP endpoints
# The Controller strictly handles HTTP traffic. It receives the request, hands it off to the Service, and returns the HTTP response. It contains no business or AI logic.

from fastapi import APIRouter, Depends, HTTPException
from domain.schemas import ChatRequest, ChatResponse
from services.agent_services import AgentService
# Create a FastAPI router
router = APIRouter(prefix="/api/v1/agent", tags=["LangChain Agent"])

# Dependency injection for the service
def get_agent_service():
    return AgentService()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest, 
    service: AgentService = Depends(get_agent_service)
):
    """
    Send a message to the LangChain AI agent and get a response.
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
        
    return service.process_chat(request)