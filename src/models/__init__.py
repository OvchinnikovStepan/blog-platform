from .models import User, Article, Comment, Tag, article_tags
from .relationships import setup_relationships

# Убедимся, что relationships настроены
setup_relationships()

__all__ = ['User', 'Article', 'Comment', 'Tag', 'article_tags']