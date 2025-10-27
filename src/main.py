from fastapi import FastAPI
from sqlalchemy import text
from src.config.database import SessionLocal

app = FastAPI(
    title="Blog Platform API",
    description="A simple blog platform built with FastAPI",
    version="1.0.0"
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
    """Health check that verifies both API and database connectivity"""
    try:
        # Проверяем подключение к БД
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy", 
            "database": "disconnected",
            "error": str(e)
        }, 503

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)