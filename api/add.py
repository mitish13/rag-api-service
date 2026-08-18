import uuid

from fastapi import APIRouter, File, HTTPException, UploadFile
from qdrant_client.models import PointStruct

from config import settings
from services.chunker import chunk_text
from services.document import extract_text
from services.embeddings import embed_documents
from services.qdrant import upsert_points


router = APIRouter(
    prefix="/add",
    tags=["documents"],
)


@router.post("")
async def add_document(
    file: UploadFile = File(...)
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required",
        )

    try:
        content = await file.read()

        pages = extract_text(
            file.filename,
            content,
        )

        all_chunks = []

        for page in pages:
            chunks = chunk_text(
                page["text"],
                chunk_size=settings.chunk_size,
                overlap=settings.chunk_overlap,
            )

            for chunk in chunks:
                all_chunks.append(
                    {
                        "text": chunk,
                        "page": page["page"],
                    }
                )

        if not all_chunks:
            raise HTTPException(
                status_code=400,
                detail="No text could be extracted from the document",
            )

        texts = [
            chunk["text"]
            for chunk in all_chunks
        ]

        embeddings = embed_documents(texts)

        document_id = str(uuid.uuid4())

        points = []

        for index, (chunk, embedding) in enumerate(
            zip(all_chunks, embeddings)
        ):
            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={
                        "document_id": document_id,
                        "filename": file.filename,
                        "chunk_id": index,
                        "page": chunk["page"],
                        "text": chunk["text"],
                    },
                )
            )

        upsert_points(points)

        return {
            "message": "Document added successfully",
            "document_id": document_id,
            "filename": file.filename,
            "chunks_created": len(points),
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )