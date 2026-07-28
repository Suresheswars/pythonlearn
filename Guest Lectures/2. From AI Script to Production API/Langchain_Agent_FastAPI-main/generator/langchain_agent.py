# Core LLM/LangChain logic (The "Brain")
# This encapsulates all the LangChain logic. By keeping this isolated, if you ever want to switch from OpenAI to Anthropic or add complex tools, you only touch this file.

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

class SimpleAgentGenerator:
    def __init__(self, api_key: str):
        # Initialize the LLM
        self.llm = ChatOpenAI(
            temperature=0.7, 
            openai_api_key=api_key,
            model="gpt-3.5-turbo"
        )
        
        # Define the system's persona and prompt
        self.prompt = PromptTemplate(
            input_variables=["query"],
            template="You are a highly intelligent and helpful tutor. Answer the student's query clearly and concisely.\n\nQuery: {query}"
        )
        
        # Create a simple chain: Prompt -> LLM -> String Output
        self.chain = self.prompt | self.llm | StrOutputParser()

    def generate_response(self, query: str) -> str:
        """Invokes the LangChain sequence with the user's query."""
        try:
            # Execute the chain
            response = self.chain.invoke({"query": query})
            return response
        except Exception as e:
            # Handle potential API errors gracefully
            return f"Error generating response: {str(e)}"