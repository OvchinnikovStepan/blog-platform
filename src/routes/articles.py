from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.schemas.article import ArticleCreate, ArticleUpdate, ArticleResponse, ArticleListResponse
from src.controllers.articles import ArticleController
from src.utils.auth import get_current_user
from src.models.models import User

router = APIRouter()

@router.post("/articles", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
def create_article(
    article_data: ArticleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    article = ArticleController.create_article(article_data, current_user, db)
    return ArticleResponse.from_orm(article)

@router.get("/articles", response_model=ArticleListResponse)
def get_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    articles = ArticleController.get_articles(db, skip, limit)
    article_responses = [ArticleResponse.from_orm(article) for article in articles]
    return {"articles": article_responses, "articles_count": len(article_responses)}

# ОСНОВНОЙ ЭНДПОИНТ: Получение статьи по ID
@router.get("/articles/{article_id}", response_model=ArticleResponse)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = ArticleController.get_article_by_id(article_id, db)
    return ArticleResponse.from_orm(article)

@router.put("/articles/{article_id}", response_model=ArticleResponse)
def update_article(
    article_id: int,
    article_data: ArticleUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    article = ArticleController.update_article(article_id, article_data, current_user, db)
    return ArticleResponse.from_orm(article)

# Мягкое удаление статьи по ID
@router.delete("/articles/{article_id}")
def soft_delete_article(
    article_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return ArticleController.soft_delete_article(article_id, current_user, db)