from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from src.schemas.user import UserResponse

class CommentBase(BaseModel):
    """Базовая схема комментария"""
    body: str

class CommentCreate(CommentBase):
    """Схема создания комментария"""
    pass

class CommentResponse(CommentBase):
    """Схема ответа на запрос о комментарии"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    author: UserResponse
    
    class Config:
        from_attributes = True