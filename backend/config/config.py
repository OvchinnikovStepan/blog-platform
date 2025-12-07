import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../backend/.env'))

class Settings:
    """Настройки приложения из переменных окружения"""
    
    # База данных
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql+asyncpg://blog_user:blog_password@postgres:5432/blog_db"
    )
    
    # JWT
    JWT_SECRET: str = os.getenv(
        "JWT_SECRET", 
        "secret-key"
    )
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Приложение
    APP_NAME: str = os.getenv("APP_NAME", "Blog Platform API")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # CORS
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")

# Создаем экземпляр настроек
settings = Settings()