# DocMind — Context-Aware Document QA System

> Retrieval-Augmented Generation pipeline for question answering over custom document corpora.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-latest-orange?style=flat-square)
![LLaMA3](https://img.shields.io/badge/LLaMA-3-purple?style=flat-square)
![ChromaDB](https://img.shields.io/badge/ChromaDB-latest-red?style=flat-square)

---

## Overview

DocMind is a local RAG (Retrieval-Augmented Generation) system that lets you upload any document and ask natural language questions about its content. It uses LangChain for orchestration, ChromaDB as a vector store, and LLaMA 3 (via Ollama) as the language model — all exposed through a RESTful FastAPI interface and a clean browser-based frontend.

---

## Features

- Upload `.txt`, `.pdf`, or `.docx` documents via drag & drop
- Semantic chunking and embedding using `sentence-transformers/all-MiniLM-L6-v2`
- Vector similarity search with ChromaDB
- Context-aware answers powered by LLaMA 3 running locally via Ollama
- RESTful API with FastAPI
- Minimal frontend — no frameworks, no build step

---

## Project Structure

```
DocMind/
├── data/                    # Uploaded documents stored here
├── frontend/
│   ├── index.html           # UI — upload + query interface
│   ├── style.css            # Styling
│   └── app.js               # Fetch calls to the API
├── src/
│   ├── api.py               # FastAPI app — /upload and /query endpoints
│   ├── loader.py            # Document loading and chunking
│   ├── embeddings.py        # HuggingFace embedding model setup
│   ├── vector_store.py      # ChromaDB create and load
│   ├── retriever.py         # Similarity search utility
│   └── rag_pipeline.py      # LangChain RAG chain
├── arag.py                  # Entry point (CLI usage)
├── main.py                  # Alternative entry point
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally
- LLaMA 3 pulled via Ollama:

```bash
ollama pull llama3
```

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/ahmedharidy2004/DocMind.git
cd DocMind

# 2. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Usage

### 1. Start Ollama
Make sure Ollama is running in the background before starting the API:
```bash
ollama serve
```

### 2. Start the API
```bash
cd src
uvicorn api:app --reload
```
API will be available at `http://127.0.0.1:8000`

### 3. Open the Frontend
Open `frontend/index.html` directly in your browser — no server needed.

### 4. Use the Interface
- **Upload** — drag & drop or browse for a `.txt`, `.pdf`, or `.docx` file → click **Index Document**
- **Ask** — type your question, adjust Top-K chunks if needed → click **Ask** or press Enter
- **Read** — the answer streams into the response panel

---

## API Reference

### `GET /`
Health check.
```json
{ "status": "DocMind API is running" }
```

### `POST /upload`
Upload and index a document.

**Request:** `multipart/form-data` with a `file` field.

**Response:**
```json
{
  "message": "'document.txt' uploaded and indexed successfully",
  "chunks": 42
}
```

### `POST /query`
Ask a question about the indexed document.

**Request:**
```json
{
  "question": "When was Cairo University Faculty of Engineering established?",
  "k": 5
}
```

**Response:**
```json
{
  "question": "When was Cairo University Faculty of Engineering established?",
  "answer": "The Faculty of Engineering at Cairo University was established in 1905.",
  "k": 5
}
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `fastapi` | REST API framework |
| `uvicorn` | ASGI server |
| `langchain` | RAG orchestration |
| `langchain-ollama` | LLaMA 3 integration |
| `langchain-chroma` | ChromaDB vector store |
| `langchain-huggingface` | Embedding model |
| `sentence-transformers` | `all-MiniLM-L6-v2` embeddings |
| `chromadb` | Local vector database |
| `pypdf` | PDF loading |
| `docx2txt` | DOCX loading |

---

## How It Works

```
User uploads document
        ↓
Loader splits it into 500-token chunks (50 overlap)
        ↓
Each chunk is embedded using all-MiniLM-L6-v2
        ↓
Embeddings stored in ChromaDB (persisted to disk)
        ↓
User asks a question
        ↓
Question embedded → Top-K similar chunks retrieved
        ↓
Chunks + question sent to LLaMA 3 via Ollama
        ↓
Answer returned to frontend
```

---

## License

MIT
