"""Модель вакансии."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from models.users import HRProfile
    from models.applications import Application


class Vacancy(Base):
    """Вакансия, привязанная к HR-пользователю."""

    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    salary: Mapped[int | None]
    experience: Mapped[str | None]
    hr_id: Mapped[int] = mapped_column(ForeignKey("hr_profiles.id"))
    hr: Mapped["HRProfile"] = relationship(back_populates="vacancies")
    applications: Mapped[list["Application"]] = relationship(
        back_populates="vacancy",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
