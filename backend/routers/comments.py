from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from schemas.comment import CommentCreate, CommentResponse
from controllers.comments import CommentController
from utils.auth import verify_token

router = APIRouter()

@router.post("/articles/{article_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    article_id: int,
    comment_data: CommentCreate,
    current_user: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    """Создание комментария к статье (требует аутентификации)"""
    return await CommentController.create_comment(article_id, comment_data, current_user, db)

@router.get("/articles/{article_id}/comments", response_model=list[CommentResponse])
async def get_comments(article_id: int, db: AsyncSession = Depends(get_db)):
    """Получение комментариев к статье (публичный)"""
    return await CommentController.get_comments_for_article(article_id, db)

@router.delete("/comments/{comment_id}")
async def soft_delete_comment(
    comment_id: int,
    current_user: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    """Мягкое удаление комментария (требует аутентификации)"""
    return await CommentController.soft_delete_comment(comment_id, current_user, db)