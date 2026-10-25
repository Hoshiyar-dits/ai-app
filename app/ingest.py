from pathlib import Path
import fitz

from app.database.chroma import collection
from app.chat.services.embedding_service import generate_embeddings

PDF_PATH = Path(__file__).resolve().parent / "policies" / "policy.pdf"


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 150) -> list[str]:
    text = " ".join(text.split())
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == len(text):
            break

        start = end - overlap

    return chunks


def ingest_policy() -> None:
    if not PDF_PATH.is_file():
        raise FileNotFoundError(
            f"Policy PDF not found: {PDF_PATH}"
        )

    with fitz.open(PDF_PATH) as pdf:
        pages = [
            (page_number, page.get_text().strip())
            for page_number, page in enumerate(pdf, start=1)
        ]

    chunks = []

    for page_number, page_text in pages:
        for chunk in chunk_text(page_text):
            chunks.append({
                "text": chunk,
                "page": page_number,
            })

    if not chunks:
        raise ValueError(
            "No extractable text found in policy.pdf. "
            "The PDF may require OCR."
        )

    batch_size = 64
    source = "policy.pdf"

    collection.delete(where={"source": source})

    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]
        texts = [item["text"] for item in batch]
        embeddings = generate_embeddings(texts)

        collection.add(
            ids=[
                f"policy-pdf-chunk-{start + i}"
                for i in range(len(batch))
            ],
            documents=texts,
            embeddings=embeddings,
            metadatas=[
                {
                    "source": source,
                    "chunk_index": start + i,
                    "page": item["page"],
                }
                for i, item in enumerate(batch)
            ],
        )

    print(f"Successfully indexed {len(chunks)} chunks from {PDF_PATH}")


if __name__ == "__main__":
    ingest_policy()
