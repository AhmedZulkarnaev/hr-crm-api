"""Маршруты API регистрации и входа пользователей."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.constants import TOKEN_TYPE_BEARER
from core.security import create_access_token, get_current_user
from db.database import get_db
from models.users import User
from schemas.users import UserCreate, UserResponse
from services.users import (
    authenticate_user,
    create_user_service,
    get_user_by_email,
)

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.post(
    "/", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email уже зарегистрирован",
        )
    return create_user_service(db=db, user_in=user)


@router.post("/login")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Авторизация по email и паролю; возвращает access token."""
    user = authenticate_user(db, form_data.username, form_data.password)
    print(f"Пытаемся войти: {form_data.username} / {form_data.password}")
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Неверный email или пароль",
        )
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": TOKEN_TYPE_BEARER}


@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    """
    Возвращает информацию о текущем авторизованном пользователе.
    Доступно только с JWT токеном.
    """
    return current_user
