from src.config.database import SessionLocal
from src.models.models import User, Article, Tag, Comment
from src.config.auth import get_password_hash

def update_test_data():
    db = SessionLocal()
    
    try:
        print("🔄 Updating test data with new fields...")
        
        # Обновляем существующего пользователя
        user = db.query(User).filter(User.email == "test@example.com").first()
        if user:
            user.is_active = True
            print("✅ User updated with is_active field")
        
        # Обновляем существующую статью
        article = db.query(Article).filter(Article.slug == "my-first-blog-post").first()
        if article:
            article.is_deleted = False
            print("✅ Article updated with is_deleted field")
        
        # Обновляем существующий комментарий
        comment = db.query(Comment).first()
        if comment:
            comment.is_deleted = False
            print("✅ Comment updated with is_deleted field")
        
        db.commit()
        print("🎉 Test data updated successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error updating test data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    update_test_data()