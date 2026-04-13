"""Модель пользователя (кандидат или HR)."""

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.constants import ROLE_CANDIDATE
from db.base import Base

if TYPE_CHECKING:
    from models.vacancies import Vacancy


class User(Base):
    """Учётная запись: роль, связь с созданными вакансиями (для HR)."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str | None]
    role: Mapped[str] = mapped_column(default=ROLE_CANDIDATE)
    vacancies: Mapped[list["Vacancy"]] = relationship(back_populates="hr")
