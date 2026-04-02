"""Схемы Pydantic для вакансий."""

from pydantic import BaseModel, ConfigDict


class VacancyCreate(BaseModel):
    """Создание вакансии: заголовок, описание, зарплата."""

    title: str
    description: str
    salary: int | None = None


class VacancyResponse(BaseModel):
    """Вакансия в ответе API."""

    id: int
    title: str
    description: str
    salary: int | None
    hr_id: int

    model_config = ConfigDict(from_attributes=True)
