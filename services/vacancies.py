"""Сервисная логика вакансий."""

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.vacancies import Vacancy
from schemas.vacancies import VacancyCreate


def get_all_vacancies_service(db: Session) -> Sequence[Vacancy]:
    """Возвращает все вакансии из БД."""
    query = select(Vacancy)
    return db.scalars(query).all()


def create_vacancy_service(
    db: Session,
    vacancy_in: VacancyCreate,
    hr_id: int,
) -> Vacancy:
    """Создаёт вакансию и привязывает её к HR."""
    db_vacancy = Vacancy(**vacancy_in.model_dump(), hr_id=hr_id)
    db.add(db_vacancy)
    db.commit()
    db.refresh(db_vacancy)
    return db_vacancy
