from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Базовая схема пользователя"""
    email: EmailStr
    username: str
    
class UserCreate(UserBase):
    """Схема для создания пользователя"""
    password: str

class UserUpdate(BaseModel):
    """Схема для изменения пользователя"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    bio: Optional[str] = None
    image_url: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    """Схема ответа с данными пользователя"""
    id: int
    bio: Optional[str] = None
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    """Схема для аутентификации пользователя пользователя"""
    email: EmailStr
    password: str

class Token(BaseModel):
    """Схема ответа на запрос аутенитификации"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None