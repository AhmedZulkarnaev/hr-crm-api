"""Схемы Pydantic для откликов."""

from pydantic import BaseModel, ConfigDict


class ApplicationCreate(BaseModel):
    """Данные для создания отклика."""

    vacancy_id: int
    cover_letter: str | None = None


class ApplicationResponse(BaseModel):
    """Отклик в ответе API."""

    id: int
    candidate_id: int
    vacancy_id: int
    cover_letter: str | None
    status: str

    model_config = ConfigDict(from_attributes=True)


class ApplicationStatusUpdate(BaseModel):
    """Смена статуса отклика (для HR)."""

    status: str
