from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User
from app.models.ai_support import AISupportChat

from app.schemas.ai_support import (
    AISupportRequest,
    AISupportResponse,
)

from app.services.ai_support_service import (
    get_ai_response
)


router = APIRouter(
    prefix="/api/ai-support",
    tags=["AI Support"]
)


@router.post(
    "/",
    response_model=AISupportResponse
)
def ai_support(
    request: AISupportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    ai_response = get_ai_response(
        request.message
    )

    chat = AISupportChat(
        user_id=current_user.id,
        question=request.message,
        ai_response=ai_response
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat