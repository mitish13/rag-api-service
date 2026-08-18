# RAG API SERVICE

A local Retrieval-Augmented Generation backend built with Python and FastAPI.

## Features

- PDF document ingestion
- TXT document ingestion
- Text chunking
- Local BGE embeddings
- Qdrant vector database
- Semantic document retrieval
- Local LLM inference with Ollama
- Source/page references
- REST API
- Automated tests
- No paid AI APIs required

## Architecture
```markdown
PDF/TXT
   ↓
Text Extraction
   ↓
Chunking
   ↓
BGE Embeddings
   ↓
Qdrant
   ↓
Semantic Search
   ↓
Context Construction
   ↓
Ollama LLM
   ↓
Answer
```
## Technologies

- Python
- FastAPI
- Uvicorn
- Sentence Transformers
- BGE-small-en-v1.5
- Qdrant
- Ollama
- PyMuPDF
- Docker
- pytest

## Requirements

- Python 3.11+
- Docker
- Ollama

## Installation

Clone the repository:

```bash
git clone https://github.com/mitish13/rag-api-service.git
cd rag-api-service
```
Create environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
Install dependencies:
```bash
pip install -r requirements.txt
```
Start Qdrant:
```bash
docker compose up -d
```
Install/pull the Ollama model:
```bash
ollama pull gemma4
```
Start API:
``` uvicorn app.main:app --reload ```

## API documentation:
http://127.0.0.1:8000/docs
### Endpoints
1. ```GET /health```:
Checks whether the API is running.
2. ```POST /add```: 
Uploads a PDF or TXT document.
Example response:
{
  "message": "Document added successfully",
  "document_id": "abc123",
  "filename": "resume.pdf",
  "chunks_created": 12
}
3. ```POST /ask```:
Ask a question about uploaded documents.
Request:
{
  "question": "What Python experience do I have?"
}
Response:
{
  "answer": "The document states...",
  "sources": [
    {
      "filename": "resume.pdf",
      "page": 2,
      "chunk_id": 4,
      "score": 0.82
    }
  ]
}

## Design
The application intentionally does not maintain conversational memory.
Each /ask request is independent and retrieves relevant document chunks from Qdrant.

## Future Improvements
* Reranking
* Hybrid search
* Document deletion
* Document filtering
* Authentication
* PostgreSQL metadata storage
* Evaluation pipeline
* Dockerized API
* CI/CD