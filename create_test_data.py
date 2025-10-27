from src.config.database import SessionLocal
from src.models.models import User, Article, Tag, Comment

def create_test_data():
    db = SessionLocal()
    
    try:
        print("🗃️ Creating test data...")
        
        # Создаем тестового пользователя (без пароля для теста)
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password="test_password_hash",  # Простой хеш для теста
            bio="Test user bio",
            image_url="https://example.com/avatar.jpg"
        )
        db.add(user)
        db.flush()
        print("✅ Test user created")
        
        # Создаем теги
        tags = []
        tag_names = ["python", "fastapi", "docker", "programming"]
        
        for tag_name in tag_names:
            tag = Tag(name=tag_name)
            db.add(tag)
            tags.append(tag)
            print(f"✅ Tag '{tag_name}' created")
        
        db.flush()
        
        # Создаем статью
        article = Article(
            title="My First Blog Post",
            slug="my-first-blog-post",
            description="This is my first blog post using FastAPI",
            body="This is the full content of my first blog post. It's about building REST APIs with FastAPI and Docker.",
            author_id=user.id,
            tags=tags[:2]  # Используем первые два тега
        )
        db.add(article)
        db.flush()
        print("✅ Test article created")
        
        # Создаем комментарий
        comment = Comment(
            body="Great article! Thanks for sharing.",
            article_id=article.id,
            author_id=user.id
        )
        db.add(comment)
        print("✅ Test comment created")
        
        db.commit()
        print("🎉 All test data created successfully!")
        
        # Показываем созданные данные
        print(f"\n📊 Created:")
        print(f"  - User: {user.username} ({user.email})")
        print(f"  - Article: {article.title}")
        print(f"  - Tags: {[tag.name for tag in tags]}")
        print(f"  - Comment: {comment.body}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating test data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()