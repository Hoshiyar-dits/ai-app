from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ollama_host: str = "http://localhost:11434"
    chat_model: str = "llama3.2"
    embedding_model: str = "nomic-embed-text"

    chroma_path: str = "./chroma_db"
    collection_name: str = "abc_organization_policies"

    retrieval_top_k: int = 5
    temperature: float = 0.0

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

settings = Settings()
