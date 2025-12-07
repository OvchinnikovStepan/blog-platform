from sqlalchemy.orm import relationship
from .models import Article, Comment

# Настраиваем relationships после определения всех моделей
def setup_relationships():
    
    Article.comments = relationship("Comment", back_populates="article", cascade="all, delete-orphan")
    Article.tags = relationship("Tag", secondary="article_tags", backref="articles")
    
    Comment.article = relationship("Article", back_populates="comments")
setup_relationships()