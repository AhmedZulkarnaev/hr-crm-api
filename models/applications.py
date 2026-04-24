"""Модель отклика кандидата на вакансию."""

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


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
            "candidate_id", "vacancy_id", name="unique_user_application"
        ),
    )
