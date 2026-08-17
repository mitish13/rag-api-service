from pathlib import Path

import fitz


SUPPORTED_EXTENSIONS = {".pdf", ".txt"}


def extract_text(filename: str, content: bytes) -> list[dict]:
    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    if extension == ".txt":
        text = content.decode("utf-8", errors="ignore")

        return [
            {
                "text": text,
                "page": None,
            }
        ]

    if extension == ".pdf":
        return extract_pdf(content)

    raise ValueError("Unsupported file type")


def extract_pdf(content: bytes) -> list[dict]:
    document = fitz.open(
        stream=content,
        filetype="pdf",
    )

    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text").strip()

        if text:
            pages.append(
                {
                    "text": text,
                    "page": page_number,
                }
            )

    document.close()

    return pages