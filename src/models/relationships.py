from sqlalchemy.orm import relationship
from .models import User, Article, Comment

# Настраиваем relationships после определения всех моделей
def setup_relationships():
    User.articles = relationship("Article", back_populates="author")
    User.comments = relationship("Comment", back_populates="author")
    
    Article.author = relationship("User", back_populates="articles")
    Article.comments = relationship("Comment", back_populates="article", cascade="all, delete-orphan")
    Article.tags = relationship("Tag", secondary="article_tags", backref="articles")
    
    Comment.article = relationship("Article", back_populates="comments")
    Comment.author = relationship("User", back_populates="comments")

setup_relationships()