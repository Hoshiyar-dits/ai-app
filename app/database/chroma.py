import chromadb
from app.core.config import settings

chroma_client = chromadb.PersistentClient(
    path=settings.chroma_path,
)

collection = chroma_client.get_or_create_collection(
    name=settings.collection_name,
    metadata={"hnsw:space": "cosine"},
)
