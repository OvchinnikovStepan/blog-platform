from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from src.schemas.user import UserResponse

class CommentBase(BaseModel):
    body: str

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    author: UserResponse
    
    class Config:
        from_attributes = True