"""Модель отклика кандидата на вакансию."""

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class Application(Base):
    """Отклик пользователя на вакансию (статус, сопроводительное письмо)."""

    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.id"))
    cover_letter: Mapped[str | None]
    status: Mapped[str] = mapped_column(default="applied")

    __table_args__ = (
        UniqueConstraint(
            "candidate_id", "vacancy_id", name="unique_user_application"
        ),
    )
