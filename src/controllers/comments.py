from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from src.models.models import Comment, Article, User
from src.schemas.comment import CommentCreate

class CommentController:
    @staticmethod
    def create_comment(article_id: int, comment_data: CommentCreate, author: User, db: Session):
        article = db.query(Article).filter(
            Article.id == article_id,
            Article.is_deleted == False
        ).first()
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )
        
        comment = Comment(
            body=comment_data.body,
            article_id=article_id,
            author_id=author.id
        )
        
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment
    
    @staticmethod
    def get_comments_for_article(article_id: int, db: Session):
        article = db.query(Article).filter(
            Article.id == article_id,
            Article.is_deleted == False
        ).first()
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )
        
        # Получаем только НЕУДАЛЕННЫЕ комментарии
        comments = db.query(Comment).filter(
            Comment.article_id == article_id,
            Comment.is_deleted == False
        ).all()
        
        return comments
    
    @staticmethod
    def soft_delete_comment(comment_id: int, current_user: User, db: Session):
        comment = db.query(Comment).filter(
            Comment.id == comment_id,
            Comment.is_deleted == False
        ).first()
        
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found"
            )
        
        # Получаем статью для проверки прав
        article = db.query(Article).filter(
            Article.id == comment.article_id,
            Article.is_deleted == False
        ).first()
        
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )
        
        # Проверяем, что пользователь - автор комментария или статьи
        if comment.author_id != current_user.id and article.author_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this comment"
            )
        
        # Мягкое удаление комментария
        comment.is_deleted = True
        comment.deleted_at = datetime.utcnow()
        
        db.commit()
        return {"message": "Comment soft deleted successfully"}