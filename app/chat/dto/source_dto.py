from pydantic import BaseModel

class SourceDTO(BaseModel):
    document_name: str
    chunk_index: int
