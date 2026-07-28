# LangChain FastAPI Integration

A cleanly structured, production-ready REST API that integrates Large Language Models (LLMs) using LangChain and FastAPI. This project utilizes a Domain-Driven Design (DDD) inspired architecture to separate concerns and ensure high maintainability.

## 🎯 Problem Statement

As Large Language Models (LLMs) become central to modern software, developers often struggle with tightly coupled codebases where API routing, business logic, and prompt engineering are tangled together in single files. This monolithic approach leads to applications that are difficult to test, scale, and maintain. If you want to switch LLM providers or update a prompt, you risk breaking the API layer.

**The Solution:** This project solves this by implementing a layered, Clean Architecture approach. By separating the codebase into Controllers, Services, Domain schemas, and Generators, the application decouples the HTTP transport layer from the core LLM orchestration.

## 🏗️ Project Architecture

Data flows predictably through distinct layers:

1. Controllers (`/controllers`): Strictly handles HTTP requests, responses, and routing. No business logic lives here.
2. Domain (`/domain`): Defines the shape of the data using Pydantic schemas. Ensures strict data validation.
3. Service (`/services`): The "Manager". Connects the validated request from the Controller to the AI Generator, handling any business logic along the way.
4. Generator (`/generator`): The "Brain". Encapsulates all LangChain/OpenAI logic, prompt templates, and LLM chains.
5. System (`/system`): Manages application-wide configurations and environment variables securely.



### Directory Tree

```text
.
├── main.py
├── .env
├── system/
│   └── config.py
├── domain/
│   └── schemas.py
├── generator/
│   └── langchain_agent.py
├── services/
│   └── agent_service.py
└── controllers/
    └── agent_controller.py
```

## 🚀 Getting Started

### Installation

```bash
py -3.12 -m venv .venv
source .venv/bin/activate     # Mac/Linux
.venv\Scripts\activate        # Windows

pip install -r requirements.txt
```

### Configuration

```text
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### Run

```bash
uvicorn main:app --reload
```

## 🧪 Usage

Swagger:

```text
http://127.0.0.1:8000/docs
```

Sample Response:

```json
{
  "answer": "Clean Architecture separates code into distinct layers."
}
```
