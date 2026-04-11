"""Маршруты API регистрации и входа пользователей."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.security import create_access_token
from db.database import get_db
from models.users import User
from schemas.users import UserCreate, UserLogin, UserResponse
from services.users import (
    authenticate_user, create_user_service, get_user_by_email
)

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
) -> User:
    """Зарегистрировать нового пользователя."""
    existing_user = get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Данный email уже испольуется"
        )
    return create_user_service(db=db, user_in=user)


@router.post("/login")
async def login_user(
    credentials: UserLogin,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Авторизация по email и паролю; возвращает access token."""
    user = authenticate_user(db, credentials.email, credentials.password)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Неверный email или пароль",
        )
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
