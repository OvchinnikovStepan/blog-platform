from src.config.database import SessionLocal
from sqlalchemy import text

def test_database():
    print("🔍 Testing database operations...")
    
    try:
        db = SessionLocal()
        
        # Проверяем таблицы
        result = db.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """))
        tables = [row[0] for row in result.fetchall()]
        print(f"✅ Tables in database: {tables}")
        
        # Проверяем что наши таблицы созданы
        expected_tables = ['users', 'articles', 'comments', 'tags', 'article_tags']
        for table in expected_tables:
            if table in tables:
                print(f"   ✅ {table} table exists")
            else:
                print(f"   ❌ {table} table missing")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == "__main__":
    test_database()