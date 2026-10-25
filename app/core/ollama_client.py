import ollama
from app.core.config import settings

ollama_client = ollama.Client(
    host=settings.ollama_host,
)
