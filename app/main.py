
from fastapi import FastAPI
from app.chat.router import router as chat_router

app = FastAPI()

app.include_router(chat_router)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}