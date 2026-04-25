"""Модель пользователя (кандидат или HR)."""
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum, ForeignKey

from core.constants import UserRole
from db.base import Base

if TYPE_CHECKING:
    from models.applications import Application

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
    hr_profile: Mapped["HRProfile"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    candidate_profile: Mapped["CandidateProfile"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )


class HRProfile(Base):
    __tablename__ = "hr_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    company_name: Mapped[str]
    user: Mapped["User"] = relationship(back_populates="hr_profile")
    vacancies: Mapped[list["Vacancy"]] = relationship(back_populates="hr")


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    cv_url: Mapped[str | None]
    user: Mapped["User"] = relationship(back_populates="candidate_profile")
    applications: Mapped[list["Application"]] = relationship(back_populates="candidate")