from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from datetime import datetime
from models.models import Article, Tag
from schemas.article import ArticleCreate, ArticleUpdate
from utils.slug import create_slug

class ArticleController:
    """Асинхронный контроллер для операций со статьями"""
    
    @staticmethod
    async def create_article(article_data: ArticleCreate, author: dict, db: AsyncSession) -> Article:
        """Асинхронное создание статьи"""
        slug = create_slug(article_data.title)
        
        # Проверяем существующую статью
        result = await db.execute(
            select(Article).filter(
                Article.slug == slug, 
                Article.is_deleted == False
            )
        )
        existing_article = result.scalar_one_or_none()
        
        if existing_article:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Article with this title already exists"
            )

        # Обрабатываем теги
        tags = []
        for tag_name in article_data.tags:
            result = await db.execute(select(Tag).filter(Tag.name == tag_name))
            tag = result.scalar_one_or_none()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                await db.flush()
            tags.append(tag)
        
        # Создаем статью
        article = Article(
            title=article_data.title,
            slug=slug,
            description=article_data.description,
            body=article_data.body,
            author_id=author.get("id"),
        )
        
        db.add(article)
        await db.commit()

        result = await db.execute(
            select(Article)
            .options(selectinload(Article.tags))  # ← ВАЖНО: явная загрузка тегов
            .where(Article.id == article.id)
        )
        article_with_relations = result.scalar_one()

      #  await db.refresh(article)
        
        return article_with_relations
    
    @staticmethod
    async def get_articles(db: AsyncSession, skip: int = 0, limit: int = 20) -> list[Article]:
        """Асинхронное получение списка статей"""
        result = await db.execute(
            select(Article)
            .options(
                selectinload(Article.author),
                selectinload(Article.tags)
            )
            .filter(Article.is_deleted == False)
            .order_by(Article.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        articles = result.scalars().all()
        return articles
    
    @staticmethod
    async def get_article_by_id(article_id: int, db: AsyncSession) -> Article:
        """Асинхронное получение статьи по ID"""
        result = await db.execute(
            select(Article)
            .options(
                selectinload(Article.author),
                selectinload(Article.tags)
            )
            .filter(
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
        return article
    
    @staticmethod
    async def update_article(article_id: int, article_data: ArticleUpdate, current_user: dict, db: AsyncSession) -> Article:
        """Асинхронное обновление статьи"""
        result = await db.execute(
            select(Article)
            .options(selectinload(Article.tags))
            .filter(
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
        
        # Проверяем права
        if article.author_id != current_user.get("id"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this article"
            )
        
        update_data = article_data.dict(exclude_unset=True)
        
        # Обновляем slug если изменился заголовок
        if 'title' in update_data:
            new_slug = create_slug(update_data['title'])
            # Проверяем, что новый slug не занят
            result = await db.execute(
                select(Article).filter(
                    Article.slug == new_slug,
                    Article.id != article_id,
                    Article.is_deleted == False
                )
            )
            existing = result.scalar_one_or_none()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Article with this title already exists"
                )
            update_data['slug'] = new_slug
        
        # Обновляем теги
        if 'tags' in update_data:
            tags = []
            for tag_name in update_data.pop('tags'):
                result = await db.execute(select(Tag).filter(Tag.name == tag_name))
                tag = result.scalar_one_or_none()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.add(tag)
                    await db.flush()
                tags.append(tag)
            article.tags = tags
        
        # Обновляем остальные поля
        for field, value in update_data.items():
            setattr(article, field, value)
        
        await db.commit()
        await db.refresh(article)
        return article
    
    @staticmethod
    async def soft_delete_article(article_id: int, current_user: dict, db: AsyncSession) -> dict:
        """Асинхронное мягкое удаление статьи"""
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
        
        if article.author_id != current_user.get("id"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this article"
            )
        
        # Мягкое удаление
        article.is_deleted = True
        article.deleted_at = datetime.utcnow()
        
        await db.commit()
        return {"message": "Article soft deleted successfully"}