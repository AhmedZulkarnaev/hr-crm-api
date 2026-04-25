"""Схемы Pydantic для вакансий."""

from pydantic import BaseModel, ConfigDict, Field


class VacancyCreate(BaseModel):
    """Данные от HR для создания вакансии."""
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=20)
    salary: int | None = None
    experience: str | None = None


class VacancyResponse(BaseModel):
    """Полная информация о вакансии."""
    id: int
    hr_id: int
    title: str
    description: str
    salary: int | None
    experience: str | None

    model_config = ConfigDict(from_attributes=True)


class VacancyUpdate(BaseModel):
    """Частичное обновление вакансии HR-ом."""
    title: str | None = Field(default=None, min_length=5, max_length=100)
    description: str | None = Field(default=None, min_length=20)
    salary: int | None = None
    experience: str | None = None
