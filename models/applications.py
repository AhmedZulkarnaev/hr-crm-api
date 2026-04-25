"""Модель отклика кандидата на вакансию."""

from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from db.base import Base
from core.constants import  ApplicationStatus
from models.users import CandidateProfile
from  models.vacancies import Vacancy


class Application(Base):
    """Отклик пользователя на вакансию (статус, сопроводительное письмо)."""

    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidate_profiles.id", ondelete="CASCADE"))
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.id", ondelete="CASCADE"))
    cover_letter: Mapped[str | None] = mapped_column(Text)
    status: Mapped[ApplicationStatus] = mapped_column(default=ApplicationStatus.PENDING)
    applied_at: Mapped[datetime] = mapped_column(server_default=func.now())
    candidate: Mapped["CandidateProfile"] = relationship(back_populates="applications")
    vacancy: Mapped["Vacancy"] = relationship(back_populates="applications")

    __table_args__ = (
        UniqueConstraint(
            "candidate_id", "vacancy_id", name="unique_candidate_application"
        ),
    )
