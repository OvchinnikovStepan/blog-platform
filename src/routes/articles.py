from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.database import get_db
from src.schemas.article import ArticleCreate, ArticleUpdate, ArticleResponse, ArticleListResponse
from src.controllers.articles import ArticleController
from src.utils.auth import get_current_user
from src.models.models import User

router = APIRouter()

@router.post("/articles", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
async def create_article(
    article_data: ArticleCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Создание новой статьи (требует аутентификации)"""
    return await ArticleController.create_article(article_data, current_user, db)

@router.get("/articles", response_model=ArticleListResponse)
async def get_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Получение списка статей (публичный)"""
    articles = await ArticleController.get_articles(db, skip, limit)
    article_responses = [ArticleResponse.from_orm(article) for article in articles]
    return {"articles": article_responses, "articles_count": len(article_responses)}

@router.get("/articles/{article_id}", response_model=ArticleResponse)
async def get_article(article_id: int, db: AsyncSession = Depends(get_db)):
    """Получение статьи по ID (публичный)"""
    article = await ArticleController.get_article_by_id(article_id, db)
    return ArticleResponse.from_orm(article)

@router.put("/articles/{article_id}", response_model=ArticleResponse)
async def update_article(
    article_id: int,
    article_data: ArticleUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Обновление статьи (требует аутентификации и прав автора)"""
    article = await ArticleController.update_article(article_id, article_data, current_user, db)
    return ArticleResponse.from_orm(article)

@router.delete("/articles/{article_id}")
async def soft_delete_article(
    article_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Мягкое удаление статьи (требует аутентификации и прав автора)"""
    return await ArticleController.soft_delete_article(article_id, current_user, db)