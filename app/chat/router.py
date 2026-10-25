import logging
from fastapi import APIRouter, Depends, HTTPException
from app.chat.dependencies import get_chat_service
from app.chat.dto.chat_request_dto import ChatRequestDTO
from app.chat.dto.chat_response_dto import ChatResponseDTO
from app.chat.services.chat_service import ChatService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Chat"])

@router.post("/chat", response_model=ChatResponseDTO)
def chat_with_abc_policy(request: ChatRequestDTO, service: ChatService = Depends(get_chat_service)) -> ChatResponseDTO:
    try:
        result = service.ask(request.question)
        return ChatResponseDTO(**result)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        logger.exception("Failed to process ABC policy chat request")

        raise HTTPException(
            status_code=503,
            detail="Unable to process your question. Please try again.",
        ) from exc
