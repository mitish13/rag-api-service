from fastapi import FastAPI

app = FastAPI(
    title="RAG API SERVICE",
    description="A local RAG backend for asking questions about uploaded documents.",
    version="0.1.0",
)

@app.get("/")
def home():
    return{"message":"AI service is running"}

@app.get("/health")
def health():
    return{"status":"ok"}