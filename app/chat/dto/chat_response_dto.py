from pydantic import BaseModel
from app.chat.dto.source_dto import SourceDTO

class ChatResponseDTO(BaseModel):
    question: str
    answer: str
    sources: list[SourceDTO]
