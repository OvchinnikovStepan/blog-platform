from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime
from src.schemas.user import UserResponse

class ArticleBase(BaseModel):
    """Базовая схема статьи"""
    title: str
    description: str
    body: str
    tagList: Optional[List[str]] = []

class ArticleCreate(ArticleBase):
    """Схема создания статьи (идентична базовой)"""
    pass

class ArticleUpdate(BaseModel):
    """Схема редактирования статьи"""
    title: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None
    tagList: Optional[List[str]] = None

class ArticleResponse(ArticleBase):
    """Схема ответа на запрос по статье"""
    slug: str
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    author: UserResponse
    tags: List[str] = [] 
    
    class Config:
        from_attributes = True

    @field_validator('tags', mode='before')
    @classmethod
    def convert_tags_to_strings(cls, v):
        """Конвертируем объекты Tag в строки"""
        if v and isinstance(v[0], object) and hasattr(v[0], 'name'):
            # Если это список объектов Tag, извлекаем имена
            return [tag.name for tag in v]
        return v

    @field_validator('tagList', mode='before')
    @classmethod
    def convert_taglist_to_strings(cls, v):
        """Конвертируем tagList в строки"""
        if v and isinstance(v[0], object) and hasattr(v[0], 'name'):
            return [tag.name for tag in v]
        return v

class ArticleListResponse(BaseModel):
    "Получение списка статей"
    articles: List[ArticleResponse]
    articles_count: int