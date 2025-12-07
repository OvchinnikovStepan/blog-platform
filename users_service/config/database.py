import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config.config import settings

# Асинхронный движок БД
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Логирование SQL запросов в debug режиме
    future=True
)

# Асинхронная фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

DeclarativeBase = declarative_base()

class Base(DeclarativeBase):
    __abstract__=True
    @classmethod
    @property
    def __tablename__(cls):
        return cls.__qualname__.lower() + "s"


# Экспортируем DATABASE_URL для обратной совместимости с миграциями
DATABASE_URL = settings.DATABASE_URL

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def create_tables():
    """Создание таблиц в БД (для миграций и тестов)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_tables():
    """Удаление таблиц (для тестов)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


from sqlalchemy import create_engine as create_sync_engine

# Синхронный движок для миграций Alembic
sync_engine = create_sync_engine(
    settings.DATABASE_URL.replace('+asyncpg', ''),  # Убираем asyncpg для синхронного подключения
    echo=settings.DEBUG
)