from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime

class ArticleBase(BaseModel):
    """Базовая схема статьи"""
    title: str
    description: str
    body: str
    tags: List[str] = [] 

class ArticleCreate(ArticleBase):
    """Схема создания статьи (идентична базовой)"""
    pass

class ArticleUpdate(BaseModel):
    """Схема редактирования статьи"""
    title: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None
    tags: Optional[List[str]] = None

class ArticleResponse(ArticleBase):
    """Схема ответа на запрос по статье"""
    slug: str
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    author_id: int
    
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


class ArticleListResponse(BaseModel):
    "Получение списка статей"
    articles: List[ArticleResponse]
    articles_count: int