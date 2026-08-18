from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "documents"

    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "gemma4"

    embedding_model: str = "BAAI/bge-small-en-v1.5"

    chunk_size: int = 800
    chunk_overlap: int = 150

    top_k: int = 5

    class Config:
        env_file = ".env"


settings = Settings()

# this file act as the guide for all the knobs of the application. 
# If .env is visible then it will override values from this file. CASE INSENSITIVE 
# Also one can import all the configuration through Settings()'s object into any file.