from ollama import Client

from config import settings


client = Client(
    host=settings.ollama_host
)


SYSTEM_PROMPT = """
You are a document question-answering assistant.

Answer the user's question using only the provided context.

Rules:
1. Do not invent information.
2. If the answer is not present in the context, say:
   "I could not find the answer in the provided documents."
3. Keep the answer concise and factual.
"""


def generate_answer(
    question: str,
    context: str,
) -> str:

    response = client.chat(
        model=settings.ollama_model,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": (
                    f"Context:\n\n"
                    f"{context}\n\n"
                    f"Question:\n\n"
                    f"{question}"
                ),
            },
        ],
    )

    return response.message.content