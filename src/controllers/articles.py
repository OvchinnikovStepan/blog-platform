from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from datetime import datetime
from src.models.models import Article, User, Tag
from src.schemas.article import ArticleCreate, ArticleUpdate
from src.utils.slug import create_slug

class ArticleController:
    @staticmethod
    def create_article(article_data: ArticleCreate, author: User, db: Session):
        slug = create_slug(article_data.title)
        
        # Проверяем существующую НЕУДАЛЕННУЮ статью с таким slug
        existing_article = db.query(Article).filter(
            Article.slug == slug, 
            Article.is_deleted == False
        ).first()
        if existing_article:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Article with this title already exists"
            )
        
        tags = []
        for tag_name in article_data.tagList:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                db.flush()
            tags.append(tag)
        
        article = Article(
            title=article_data.title,
            slug=slug,
            description=article_data.description,
            body=article_data.body,
            author_id=author.id,
        )
        article.tags = tags
        
        db.add(article)
        db.commit()
        db.refresh(article)
        
        return article
    
    @staticmethod
    def get_articles(db: Session, skip: int = 0, limit: int = 20):
        # Получаем только НЕУДАЛЕННЫЕ статьи
        articles = db.query(Article).options(
            joinedload(Article.author),
            joinedload(Article.tags)
        ).filter(
            Article.is_deleted == False
        ).offset(skip).limit(limit).all()
        return articles
    
    @staticmethod
    def get_article_by_id(article_id: int, db: Session):
        article = db.query(Article).options(
            joinedload(Article.author),
            joinedload(Article.tags)
        ).filter(
            Article.id == article_id,
            Article.is_deleted == False
        ).first()
        
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )
        return article
    
    @staticmethod
    def update_article(article_id: int, article_data: ArticleUpdate, current_user: User, db: Session):
        article = db.query(Article).options(
            joinedload(Article.tags)
        ).filter(
            Article.id == article_id,
            Article.is_deleted == False
        ).first()
        
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )
        
        if article.author_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this article"
            )
        
        update_data = article_data.dict(exclude_unset=True)
        
        # Если меняется заголовок, обновляем slug
        if 'title' in update_data:
            new_slug = create_slug(update_data['title'])
            # Проверяем, что новый slug не занят другой статьей
            existing = db.query(Article).filter(
                Article.slug == new_slug,
                Article.id != article_id,
                Article.is_deleted == False
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Article with this title already exists"
                )
            update_data['slug'] = new_slug
        
        if 'tagList' in update_data:
            tags = []
            for tag_name in update_data.pop('tagList'):
                tag = db.query(Tag).filter(Tag.name == tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.add(tag)
                    db.flush()
                tags.append(tag)
            article.tags = tags
        
        for field, value in update_data.items():
            setattr(article, field, value)
        
        db.commit()
        db.refresh(article)
        return article
    
    @staticmethod
    def soft_delete_article(article_id: int, current_user: User, db: Session):
        article = db.query(Article).filter(
            Article.id == article_id,
            Article.is_deleted == False
        ).first()
        
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )
        
        if article.author_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this article"
            )
        
        # Мягкое удаление - меняем статус
        article.is_deleted = True
        article.deleted_at = datetime.utcnow()
        
        db.commit()
        return {"message": "Article soft deleted successfully"}