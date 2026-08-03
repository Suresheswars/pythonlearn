from fastapi import APIRouter, UploadFile, Form
from src.backend.logger import GLOBAL_LOGGER as log
from src.shared.schemas import QueryRequest, QueryResponse
from src.backend.services.ingestion_service import ingest_document
from src.backend.services.retrieval_service import retrieve_answer


router = APIRouter()


@router.post("/upload")
async def upload(file: UploadFile, embedding_model: str = Form(...)):
    
    log.info('Upload File API Trigerred', embedding_model=embedding_model)
    chunks = await ingest_document(file, embedding_model)
    log.info('Upload File completed')
   
    return {"chunks": chunks}


@router.post("/retrieve", response_model=QueryResponse)
async def retrieve(request: QueryRequest):

    log.info('Retrieve API Trigerred', embedding_model=request.embedding_model)
    answer,answer_texts,evaluation_metric = retrieve_answer(request.question, request.embedding_model, request.retriever_type)
    log.info('Answer Retrieved')
    
    return QueryResponse(answer=answer,answer_texts=answer_texts,evaluation_metric=evaluation_metric)