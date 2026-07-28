# Business logic tying domain and generator
# The Service layer handles the business logic. It takes the validated data from the controller, passes it to the generator, and formats the result back into a domain schema.

from domain.schemas import ChatRequest, ChatResponse
from generator.langchain_agent import SimpleAgentGenerator
from system.config import settings

class AgentService:
    def __init__(self):
        # Instantiate the generator using system configurations
        print('OPENAI Key: ',settings.openai_api_key)
        self.generator = SimpleAgentGenerator(api_key=settings.openai_api_key)

    def process_chat(self, request: ChatRequest) -> ChatResponse:
        """Processes the request and coordinates with the generator."""
        # 1. Extract the query
        user_query = request.query
        
        # 2. Get the answer from the LangChain generator
        llm_answer = self.generator.generate_response(user_query)
        
        # 3. Wrap the result in our Domain Schema and return
        return ChatResponse(answer=llm_answer)