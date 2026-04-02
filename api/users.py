"""Маршруты API регистрации и входа пользователей."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from db.database import get_db
from models.users import User
from schemas.users import UserCreate, UserLogin, UserResponse

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
) -> User:
    """Зарегистрировать нового пользователя."""
    hashed_pw = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        role=user.role,
        hashed_password=hashed_pw,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login")
async def login_user(
    credentials: UserLogin,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Авторизация по email и паролю; возвращает access token."""
    query = select(User).where(User.email == credentials.email)
    db_user = db.scalar(query)

    if (
        db_user is None
        or db_user.hashed_password is None
        or not verify_password(credentials.password, db_user.hashed_password)
    ):
        raise HTTPException(
            status_code=401,
            detail="Неверный email или пароль",
        )

    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}
