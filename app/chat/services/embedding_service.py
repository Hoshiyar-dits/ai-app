
from app.core.config import settings
from app.core.ollama_client import ollama_client


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for a list of text strings using Ollama.

    Args:
        texts: List of text strings to convert into embeddings.

    Returns:
        A list of embedding vectors, one for each input text.
    """
    if not texts:
        return []

    response = ollama_client.embed(
        model=settings.embedding_model,
        input=texts,
    )

    return response["embeddings"]
