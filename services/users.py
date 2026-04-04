"""Сервисная логика пользователей: регистрация и аутентификация."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from core.security import get_password_hash, verify_password
from models.users import User
from schemas.users import UserCreate


def create_user_service(db: Session, user_in: UserCreate) -> User:
    """Создаёт пользователя с хешем пароля и коммитит в БД."""
    hashed_pw = get_password_hash(user_in.password)
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        role=user_in.role,
        hashed_password=hashed_pw,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """Возвращает пользователя при верном пароле, иначе None."""
    query = select(User).where(User.email == email)
    user = db.scalar(query)
    if (
        user is None
        or user.hashed_password is None
        or not verify_password(password, user.hashed_password)
    ):
        return None
    return user
