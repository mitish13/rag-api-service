from fastapi import FastAPI
from services.qdrant import initialize_collection
from contextlib import asynccontextmanager
from api.add import router as add_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs BEFORE the app starts accepting requests
    initialize_collection()
    print("Qdrant collection ready")
    
    yield  # <-- app is running here


app = FastAPI(
    title="RAG API SERVICE",
    description="A local RAG backend for asking questions about uploaded documents.",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(add_router)

    
@app.get("/")
def home():
    return{"message":"AI service is running"}

@app.get("/health")
def health():
    return{"status":"ok"}