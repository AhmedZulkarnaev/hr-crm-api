"""Хеширование паролей, JWT и зависимость текущего пользователя."""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.constants import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_ALGORITHM,
    JWT_SECRET_KEY,
    OAUTH2_TOKEN_URL,
)
from db.database import get_db
from models.users import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=OAUTH2_TOKEN_URL)


def get_password_hash(password: str) -> str:
    """Возвращает bcrypt-хеш пароля в виде строки."""
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет открытый пароль на соответствие сохранённому хешу."""
    plain_password_bytes = plain_password.encode("utf-8")
    hashed_password_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)


def create_access_token(data: dict) -> str:
    """Создаёт JWT access token с полем exp."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Извлекает пользователя из Bearer-токена или возвращает 401."""
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Неверный токен")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Токен протух или сломан")
    user = db.get(User, int(user_id))
    if user is None:
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    return user
