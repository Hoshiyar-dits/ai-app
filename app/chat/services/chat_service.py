from app.core.config import settings
from app.chat.services.llm_service import llm_service
from app.chat.services.retrieval_service import retrieval_service

class ChatService:
    def __init__(self):
        self.retriever = retrieval_service
        self.llm = llm_service

    def ask(self, question: str) -> dict:
        question = question.strip()

        if not question:
            raise ValueError("Question cannot be empty.")

        if self._collection_is_empty():
            return {
                "question": question,
                "answer": (
                    "No policy documents are indexed yet. "
                    "Please upload an ABC policy document first."
                ),
                "sources": [],
            }

        context, sources = self.retriever.retrieve(question)

        if not context:
            return {
                "question": question,
                "answer": (
                    "I couldn't find relevant policy information "
                    "to answer your question."
                ),
                "sources": [],
            }

        answer = self.llm.generate_answer(
            question=question,
            context=context,
        )

        return {
            "question": question,
            "answer": answer,
            "sources": sources,
        }

    @staticmethod
    def _collection_is_empty() -> bool:
        from app.database.chroma import collection
        return collection.count() == 0


chat_service = ChatService()
