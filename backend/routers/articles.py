from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from schemas.article import ArticleCreate, ArticleUpdate, ArticleResponse, ArticleListResponse, ArticlePreview
from controllers.articles import ArticleController
from utils.auth import verify_token
from utils.internal_auth import verify_internal_token

router = APIRouter()

@router.post("/articles", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
async def create_article(
    article_data: ArticleCreate,
    current_user: dict = Depends(verify_token),
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

@router.get("/articles/my", response_model=ArticleListResponse)
async def get_my_posts(
    current_user: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    return await ArticleController.get_users_articles(current_user, db)

@router.get("/articles/{article_id}", response_model=ArticleResponse)
async def get_article(article_id: int, db: AsyncSession = Depends(get_db)):
    """Получение статьи по ID (публичный)"""
    article = await ArticleController.get_article_by_id(article_id, db)
    return ArticleResponse.from_orm(article)

@router.put("/articles/{article_id}", response_model=ArticleResponse)
async def update_article(
    article_id: int,
    article_data: ArticleUpdate,
    current_user: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    """Обновление статьи (требует аутентификации и прав автора)"""
    article = await ArticleController.update_article(article_id, article_data, current_user, db)
    return ArticleResponse.from_orm(article)

@router.delete("/articles/{article_id}")
async def soft_delete_article(
    article_id: int,
    current_user: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    """Мягкое удаление статьи (требует аутентификации и прав автора)"""
    return await ArticleController.soft_delete_article(article_id, current_user, db)



@router.post("/articles/{article_id}/publish", status_code=202)
async def publish_article(
    article_id: int,
    current_user: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_db),
):
    return await ArticleController.publish_article(article_id,current_user,db)

@router.post("/articles/{article_id}/reject")
async def reject_article(
    article_id: int,
    db: AsyncSession = Depends(get_db),
    service: str = Depends(verify_internal_token),
):
    return await ArticleController.reject_article(article_id,db,service)

@router.put("/articles/{article_id}/preview", response_model=ArticleResponse)
async def update_article(
    article_id: int,
    preview_url: ArticlePreview,
    service: str = Depends(verify_internal_token),
    db: AsyncSession = Depends(get_db)
):
    return await ArticleController.add_article_preview(article_id, preview_url.preview_url, service, db)

@router.post("/articles/{article_id}/complete_publish")
async def reject_article(
    article_id: int,
    db: AsyncSession = Depends(get_db),
    service: str = Depends(verify_internal_token),
):
    return await ArticleController.complete_publish_article(article_id,db,service)

@router.post("/articles/{article_id}/error")
async def mark_error(
    article_id: int,
    _: str = Depends(verify_internal_token),
    db: AsyncSession = Depends(get_db),
):
    return await ArticleController.set_error_article(article_id,db)

