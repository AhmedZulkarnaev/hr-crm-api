"""Схемы Pydantic для пользователей."""

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    """Регистрация: имя, email, роль, пароль."""

    username: str
    email: EmailStr
    role: str
    password: str


class UserResponse(BaseModel):
    """Пользователь без пароля."""

    id: int
    username: str
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    """Вход по email и паролю."""

    email: EmailStr
    password: str
