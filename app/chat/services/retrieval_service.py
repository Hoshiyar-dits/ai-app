from app.core.config import settings
from app.database.chroma import collection
from app.chat.services.llm_service import llm_service

class RetrievalService:
    def retrieve(self,question: str) -> tuple[str, list[dict]]:
        if collection.count() == 0:
            return "", []

        query_embedding = llm_service.create_embeddings([question])[0]

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=min(
                settings.retrieval_top_k,
                collection.count(),
            ),
            include=["documents", "metadatas", "distances"],
        )

        documents = (results.get("documents") or [[]])[0] or []
        metadatas = (results.get("metadatas") or [[]])[0] or []

        context_parts = []
        sources = []

        for document, metadata in zip(documents, metadatas):
            if not document or not metadata:
                continue

            source_name = metadata.get("source", "Unknown document")
            chunk_index = metadata.get("chunk_index", -1)

            context_parts.append(
                f"Source: {source_name}\n"
                f"Chunk: {chunk_index}\n"
                f"Content: {document}"
            )

            sources.append({
                "document_name": source_name,
                "chunk_index": chunk_index,
            })

        unique_sources = list({
            (source["document_name"], source["chunk_index"]): source
            for source in sources
        }.values())

        return "\n\n".join(context_parts), unique_sources

retrieval_service = RetrievalService()
