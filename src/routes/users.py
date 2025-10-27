from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.schemas.user import UserCreate, UserLogin, UserUpdate, UserResponse, Token
from src.controllers.users import UserController
from src.utils.auth import get_current_user
from src.models.models import User

router = APIRouter()

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return UserController.register_user(user_data, db)

@router.post("/users/login", response_model=Token)
def login_user(login_data: UserLogin, db: Session = Depends(get_db)):
    result = UserController.authenticate_user(login_data, db)
    return {
        "access_token": result["access_token"],
        "token_type": result["token_type"]
    }

@router.get("/user", response_model=UserResponse)
def get_current_user(current_user: User = Depends(get_current_user)):
    return UserController.get_current_user_profile(current_user)

@router.put("/user", response_model=UserResponse)
def update_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return UserController.update_user_profile(user_data, current_user, db)