import time
import psycopg2
from sqlalchemy import text  # Добавляем импорт
from src.config.database import engine, SessionLocal
from src.models.models import Base

def test_docker_postgres():
    print("🐳 Testing Docker PostgreSQL...")
    
    # Ждем пока БД запустится
    for i in range(10):
        try:
            conn = psycopg2.connect(
                host="localhost",
                port="5432",
                dbname="blog_db",
                user="blog_user",
                password="blog_password"
            )
            conn.close()
            print("✅ PostgreSQL is ready!")
            break
        except Exception as e:
            print(f"⏳ Waiting... {i+1}/10")
            time.sleep(3)
    else:
        print("❌ PostgreSQL failed to start")
        return False
    
    try:
        # Тестируем SQLAlchemy
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created!")
        
        db = SessionLocal()
        # Используем text() для SQL выражений
        result = db.execute(text("SELECT version()"))
        print(f"✅ {result.fetchone()[0]}")
        db.close()
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_docker_postgres()