from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.database import AsyncSessionLocal, settings
from src.config.config import settings as app_settings

app = FastAPI(
    title=app_settings.APP_NAME,
    description="A simple blog platform built with FastAPI",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=app_settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def setup_routes():
    from src.routes import users, articles, comments
    app.include_router(users.router, prefix="/api", tags=["users"])
    app.include_router(articles.router, prefix="/api", tags=["articles"])
    app.include_router(comments.router, prefix="/api", tags=["comments"])

# Настраиваем роуты при запуске
setup_routes()

@app.get("/")
async def root():
    return {"message": "Welcome to Blog Platform API"}

@app.get("/health")
async def health_check():
    """Health check с асинхронной проверкой БД"""
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        
        return {
            "status": "healthy",
            "database": "connected", 
            "app": app_settings.APP_NAME,
            "debug": app_settings.DEBUG
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }, 503

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=app_settings.DEBUG
    )