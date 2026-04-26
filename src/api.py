from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from loader import load_and_chunk
from vector_store import create_vector_store
from rag_pipeline import run_pipeline

app = FastAPI(title="DocMind RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(UPLOAD_DIR, exist_ok=True)


class QueryRequest(BaseModel):
    question: str
    k: int = 5


@app.get("/")
def root():
    return {"status": "DocMind API is running"}


@app.post("/upload")
def upload(file: UploadFile = File(...)):
    allowed_extensions = [".txt", ".pdf", ".docx"]
    ext = os.path.splitext(file.filename)[-1].lower()

    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: {allowed_extensions}"
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    try:
        chunks = load_and_chunk(file_path)
        create_vector_store(chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to index document: {str(e)}")

    return {
        "message": f"'{file.filename}' uploaded and indexed successfully",
        "chunks": len(chunks)
    }


@app.post("/query")
def query(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        answer = run_pipeline(request.question, model_name="llama3", k=request.k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")

    return {
        "question": request.question,
        "answer": answer,
        "k": request.k
    }