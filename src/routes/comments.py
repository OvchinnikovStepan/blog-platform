from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.schemas.comment import CommentCreate, CommentResponse
from src.controllers.comments import CommentController
from src.utils.auth import get_current_user
from src.models.models import User

router = APIRouter()

# Создание комментария к статье по ID статьи
@router.post("/articles/{article_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    article_id: int,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return CommentController.create_comment(article_id, comment_data, current_user, db)

# Получение комментариев к статье по ID статьи
@router.get("/articles/{article_id}/comments", response_model=list[CommentResponse])
def get_comments(article_id: int, db: Session = Depends(get_db)):
    return CommentController.get_comments_for_article(article_id, db)

# Мягкое удаление комментария по ID комментария
@router.delete("/comments/{comment_id}")
def soft_delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return CommentController.soft_delete_comment(comment_id, current_user, db)