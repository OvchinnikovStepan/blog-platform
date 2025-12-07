from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from datetime import datetime
from models.models import Comment, Article
from schemas.comment import CommentCreate

class CommentController:
    """Асинхронный контроллер для операций с комментариями"""
    
    @staticmethod
    async def create_comment(article_id: int, comment_data: CommentCreate, author: dict, db: AsyncSession) -> Comment:
        """Асинхронное создание комментария"""
        # Проверяем существование статьи
        result = await db.execute(
            select(Article).filter(
                Article.id == article_id,
                Article.is_deleted == False
            )
        )
        article = result.scalar_one_or_none()
        
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )
        
        # Создаем комментарий
        comment = Comment(
            body=comment_data.body,
            article_id=article_id,
            author_id=author.get("id")
        )
        
        db.add(comment)
        await db.commit()
        await db.refresh(comment)
        
        return comment
    
    @staticmethod
    async def get_comments_for_article(article_id: int, db: AsyncSession) -> list[Comment]:
        """Асинхронное получение комментариев к статье"""
        # Проверяем существование статьи
        result = await db.execute(
            select(Article).filter(
                Article.id == article_id,
                Article.is_deleted == False
            )
        )
        article = result.scalar_one_or_none()
        
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )
        
        # Получаем комментарии с информацией об авторах
        result = await db.execute(
            select(Comment)
            .options(selectinload(Comment.author))
            .filter(
                Comment.article_id == article_id,
                Comment.is_deleted == False
            )
            .order_by(Comment.created_at.desc())
        )
        comments = result.scalars().all()
        
        return comments
    
    @staticmethod
    async def soft_delete_comment(comment_id: int, current_user: dict, db: AsyncSession) -> dict:
        """Асинхронное мягкое удаление комментария"""
        # Находим комментарий
        result = await db.execute(
            select(Comment)
            .options(selectinload(Comment.article))
            .filter(
                Comment.id == comment_id,
                Comment.is_deleted == False
            )
        )
        comment = result.scalar_one_or_none()
        
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found"
            )
        
        # Проверяем права: автор комментария или автор статьи
        if comment.author_id != current_user.get("id") and comment.article.author_id != current_user.get("id"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this comment"
            )
        
        # Мягкое удаление
        comment.is_deleted = True
        comment.deleted_at = datetime.utcnow()
        
        await db.commit()
        return {"message": "Comment soft deleted successfully"}