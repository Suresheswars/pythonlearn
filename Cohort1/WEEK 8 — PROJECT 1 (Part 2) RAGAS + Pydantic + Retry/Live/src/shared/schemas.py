from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    question: str
    embedding_model: str
    retriever_type: str

class QueryResponse(BaseModel):
    answer: str
    answer_texts: list
    evaluation_metric: dict
