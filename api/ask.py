from fastapi import APIRouter, HTTPException

from config import settings
from schemas import AskRequest, AskResponse, Source
from services.embeddings import embed_query
from services.llm import generate_answer
from services.qdrant import search_vectors


router = APIRouter(
    prefix="/ask",
    tags=["questions"],
)


@router.post("", response_model=AskResponse)
def ask_question(request: AskRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty",
        )

    query_vector = embed_query(question)

    top_k = request.top_k or settings.top_k

    results = search_vectors(
        query_vector,
        limit=top_k,
    )

    if not results:
        return AskResponse(
            answer="I could not find any relevant information in the provided documents.",
            sources=[],
        )

    context_parts = []
    sources = []

    for result in results:

        payload = result.payload

        context_parts.append(
            f"""
Source: {payload["filename"]}
Page: {payload["page"]}

Content:
{payload["text"]}
"""
        )

        sources.append(
            Source(
                filename=payload["filename"],
                page=payload["page"],
                chunk_id=payload["chunk_id"],
                score=result.score,
            )
        )

    context = "\n\n---\n\n".join(context_parts)

    answer = generate_answer(
        question=question,
        context=context,
    )

    return AskResponse(
        answer=answer,
        sources=sources,
    )