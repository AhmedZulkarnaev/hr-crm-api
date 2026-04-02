"""Маршруты API откликов на вакансии."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.security import get_current_user
from db.database import get_db
from models.applications import Application
from models.users import User
from models.vacancies import Vacancy
from schemas.applications import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationStatusUpdate,
)

router = APIRouter(prefix="/applications", tags=["Отклики"])


@router.post("", response_model=ApplicationResponse)
async def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Application:
    """Создать отклик на вакансию (только для роли candidate)."""
    if current_user.role != "candidate":
        raise HTTPException(
            status_code=403,
            detail="Только кандидаты могут откликаться",
        )

    vacancy = db.get(Vacancy, application.vacancy_id)
    if not vacancy:
        raise HTTPException(status_code=404, detail="Вакансия не найдена")

    db_application = Application(
        **application.model_dump(),
        candidate_id=current_user.id,
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)

    return db_application


@router.patch("/{application_id}/status", response_model=ApplicationResponse)
async def update_application_status(
    application_id: int,
    status_data: ApplicationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Application:
    """Обновить статус отклика (только HR этой вакансии)."""
    application = db.get(Application, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Отклик не найден")
    vacancy = db.get(Vacancy, application.vacancy_id)
    if not vacancy:
        raise HTTPException(status_code=404, detail="Вакансия не найдена")
    if vacancy.hr_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Нет прав на изменение этого отклика",
        )
    application.status = status_data.status
    db.commit()
    db.refresh(application)
    return application
