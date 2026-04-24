"""Модель пользователя (кандидат или HR)."""

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum

from core.constants import UserRole
from db.base import Base

from models.vacancies import Vacancy


class User(Base):
    """Учётная запись: роль, связь с созданными вакансиями (для HR)."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str | None]
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole),
        default=UserRole.CANDIDATE,
        nullable=False
    )
    hr_profile: Mapped["HRProfile"] = relationship(back_populates="user", uselist=False)
    candidate_profile: Mapped["CandidateProfile"] = relationship(back_populates="user", uselist=False)


class HRProfile(Base):
    __tablename__ = "hr_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    company_name: Mapped[str]
    user: Mapped["User"] = relationship(back_populates="hr_profile")
    vacancies: Mapped[list["Vacancy"]] = relationship(back_populates="hr")
