from datetime import datetime

from pydantic import BaseModel


class AISupportRequest(BaseModel):

    message: str


class AISupportResponse(BaseModel):

    id: int
    question: str
    ai_response: str
    created_at: datetime

    class Config:
        from_attributes = True