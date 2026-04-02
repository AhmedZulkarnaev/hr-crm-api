"""Маршруты API вакансий и откликов по вакансии."""

from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.security import get_current_user
from db.database import get_db
from models.applications import Application
from models.users import User
from models.vacancies import Vacancy
from schemas.applications import ApplicationResponse
from schemas.vacancies import VacancyCreate, VacancyResponse

router = APIRouter(prefix="/vacancies", tags=["Вакансии"])


@router.get("/", response_model=list[VacancyResponse])
async def get_all_vacancies(
    db: Session = Depends(get_db),
) -> Sequence[Vacancy]:
    """Список всех вакансий."""
    query = select(Vacancy)
    return db.scalars(query).all()


@router.post("/", response_model=VacancyResponse)
async def create_vacancy(
    vacancy: VacancyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Vacancy:
    """Создать вакансию (только для роли hr)."""
    if current_user.role != "hr":
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    db_vacancy = Vacancy(**vacancy.model_dump(), hr_id=current_user.id)
    db.add(db_vacancy)
    db.commit()
    db.refresh(db_vacancy)

    return db_vacancy


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
