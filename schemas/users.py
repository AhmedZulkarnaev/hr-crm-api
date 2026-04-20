"""Схемы Pydantic для пользователей."""

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from core.constants import UserRole


class UserCreate(BaseModel):
    """Регистрация: имя, email, роль, пароль."""

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    role: UserRole = UserRole.CANDIDATE
    password: str = Field(..., min_length=8)


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
