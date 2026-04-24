"""Схемы Pydantic для откликов."""

from pydantic import BaseModel, ConfigDict, Field

from datetime import datetime

from core.constants import  ApplicationStatus


class ApplicationCreate(BaseModel):
    """Кандидат отправляет отклик."""
    vacancy_id: int
    cover_letter: str | None = Field(default=None, max_length=5000)


class ApplicationResponse(BaseModel):
    """Отображение отклика."""
    id: int
    candidate_id: int
    vacancy_id: int
    cover_letter: str | None
    status: ApplicationStatus
    applied_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ApplicationStatusUpdate(BaseModel):
    """HR меняет статус отклика."""
    status: ApplicationStatus
