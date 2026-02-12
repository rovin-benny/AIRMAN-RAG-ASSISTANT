from fastapi import FastAPI
from pydantic import BaseModel
from .ingest import process_pdfs
from .engine import get_answer
import os

app = FastAPI(title="AIRMAN Aviation RAG")

class QueryRequest(BaseModel):
    question: str
    debug: bool = False

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/ingest")
def ingest_documents():
    if os.path.exists("index/faiss_store"):
        return {"message": "Index already exists. Skipping ingestion."}
    msg = process_pdfs()
    return {"message": msg}

@app.post("/ask")
def ask_question(request: QueryRequest):
    result = get_answer(request.question, request.debug)
    return result