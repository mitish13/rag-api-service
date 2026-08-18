from sentence_transformers import SentenceTransformer

from config import settings


model = SentenceTransformer(
    settings.embedding_model
)


def embed_documents(texts: list[str]) -> list[list[float]]:
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
    )

    return embeddings.tolist()


def embed_query(text: str) -> list[float]:
    embedding = model.encode(
        text,
        normalize_embeddings=True,
    )

    return embedding.tolist()