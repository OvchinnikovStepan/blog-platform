from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from schemas.user import UserCreate, UserLogin, UserUpdate, UserResponse, Token
from controllers.users import UserController
from utils.auth import get_current_user
from models.models import User

router = APIRouter()

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate, 
    db: AsyncSession = Depends(get_db)
):
    """Регистрация нового пользователя"""
    return await UserController.register_user(user_data, db)

@router.post("/users/login", response_model=Token)
async def login_user(
    login_data: UserLogin, 
    db: AsyncSession = Depends(get_db)
):
    """Аутентификация пользователя"""
    result = await UserController.authenticate_user(login_data, db)
    return {
        "access_token": result["access_token"],
        "token_type": result["token_type"]
    }

@router.get("/users/me", response_model=UserResponse)
async def get_current_user(current_user: User = Depends(get_current_user)):
    """Получение профиля текущего пользователя"""
    return await UserController.get_current_user_profile(current_user)

@router.put("/users/me", response_model=UserResponse)
async def update_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Обновление профиля пользователя"""
    return await UserController.update_user_profile(user_data, current_user, db)

