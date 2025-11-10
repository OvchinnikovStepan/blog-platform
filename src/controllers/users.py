from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from src.models.models import User
from src.schemas.user import UserCreate, UserLogin, UserUpdate
from src.config.auth import verify_password, get_password_hash, create_access_token
from datetime import timedelta
from src.config.config import settings

class UserController:
    """Асинхронный контроллер для операций с пользователями"""
    
    @staticmethod
    async def register_user(user_data: UserCreate, db: AsyncSession) -> User:
        """Асинхронная регистрация пользователя"""
        # Проверяем, существует ли пользователь
        result = await db.execute(
            select(User).filter(
                (User.email == user_data.email) | (User.username == user_data.username)
            )
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email or username already exists"
            )
        
        # Создаем нового пользователя
        hashed_password = get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password
        )
        
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        return user
    
    @staticmethod
    async def authenticate_user(login_data: UserLogin, db: AsyncSession) -> dict:
        """Асинхронная аутентификация пользователя"""
        result = await db.execute(
            select(User).filter(User.email == login_data.email)
        )
        user = result.scalar_one_or_none()
        
        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Создаем токен
        access_token = create_access_token(
            data={"user_id": user.id},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
    
    @staticmethod
    async def get_current_user_profile(current_user: User) -> User:
        """Получение профиля текущего пользователя"""
        return current_user
    
    @staticmethod
    async def update_user_profile(user_data: UserUpdate, current_user: User, db: AsyncSession) -> User:
        """Асинхронное обновление профиля пользователя"""
        update_data = user_data.dict(exclude_unset=True)
        
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        for field, value in update_data.items():
            setattr(current_user, field, value)
        
        await db.commit()
        await db.refresh(current_user)
        return current_user