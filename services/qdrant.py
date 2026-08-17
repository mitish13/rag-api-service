from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from config import settings


VECTOR_SIZE = 384

client = QdrantClient(
    url=settings.qdrant_url
)


def initialize_collection():
    collections = client.get_collections().collections

    exists = any(
        collection.name == settings.qdrant_collection
        for collection in collections
    )

    if not exists:
        client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )


def upsert_points(points: list[PointStruct]):
    client.upsert(
        collection_name=settings.qdrant_collection,
        points=points,
        wait=True,
    )


def search_vectors(
    vector: list[float],
    limit: int = 5,
):
    return client.query_points(
        collection_name=settings.qdrant_collection,
        query=vector,
        limit=limit,
    ).points