"""Маршруты API вакансий и откликов по вакансии."""

from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.constants import ROLE_HR
from core.security import get_current_user
from db.database import get_db
from models.applications import Application
from models.users import User
from models.vacancies import Vacancy
from schemas.applications import ApplicationResponse
from schemas.vacancies import VacancyCreate, VacancyResponse
from services.vacancies import (
    create_vacancy_service,
    get_all_vacancies_service,
)

router = APIRouter(prefix="/vacancies", tags=["Вакансии"])


@router.get("/", response_model=list[VacancyResponse])
async def get_all_vacancies(
    db: Session = Depends(get_db),
) -> Sequence[Vacancy]:
    """Список всех вакансий."""
    return get_all_vacancies_service(db)


@router.post("/", response_model=VacancyResponse)
async def create_vacancy(
    vacancy: VacancyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Vacancy:
    """Создать вакансию (только для роли hr)."""
    if current_user.role != ROLE_HR:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    return create_vacancy_service(
        db=db,
        vacancy_in=vacancy,
        hr_id=current_user.id,
    )


@router.get(
    "/{vacancy_id}/applications",
    response_model=list[ApplicationResponse],
)
async def get_vacancy_applications(
    vacancy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Sequence[Application]:
    """Отклики на вакансию (только владелец вакансии)."""
    vacancy = db.get(Vacancy, vacancy_id)
    if not vacancy:
        raise HTTPException(status_code=404, detail="Вакансия не найдена")

    if vacancy.hr_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Вы не можете смотреть отклики на чужую вакансию",
        )

    query = select(Application).where(Application.vacancy_id == vacancy_id)

    return db.scalars(query).all()
