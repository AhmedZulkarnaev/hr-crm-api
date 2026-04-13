"""Маршруты API откликов на вакансии."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.constants import (
    APPLICATION_NOT_FOUND,
    FORBIDDEN,
    ROLE_CANDIDATE,
    ROLE_HR,
    VACANCY_NOT_FOUND,
)
from core.security import get_current_user
from db.database import get_db
from models.applications import Application
from models.users import User
from schemas.applications import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationStatusUpdate,
)
from services.applications import (
    create_application as create_application_service,
    update_application_status_service,
)

router = APIRouter(prefix="/applications", tags=["Отклики"])


@router.post("", response_model=ApplicationResponse)
async def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Application | None:
    """Создать отклик на вакансию (только для роли candidate)."""
    if current_user.role != ROLE_CANDIDATE:
        raise HTTPException(
            status_code=403,
            detail="Только кандидаты могут откликаться",
        )

    db_application = create_application_service(
        db=db,
        application=application,
        current_user=current_user.id,
    )

    if db_application is None:
        raise HTTPException(status_code=404, detail="Вакансия не найдена")

    return db_application


@router.patch("/{application_id}/status", response_model=ApplicationResponse)
async def update_application_status(
    application_id: int,
    status_data: ApplicationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Application | None:
    """Обновить статус отклика (только HR этой вакансии)."""
    if current_user.role != ROLE_HR:
        raise HTTPException(
            status_code=403,
            detail="Только HR может менять статус отклика",
        )

    updated, error = update_application_status_service(
        db=db,
        application_id=application_id,
        new_status=status_data.status,
        hr_id=current_user.id,
    )

    if error == APPLICATION_NOT_FOUND:
        raise HTTPException(status_code=404, detail="Отклик не найден")
    if error == VACANCY_NOT_FOUND:
        raise HTTPException(status_code=404, detail="Вакансия не найдена")
    if error == FORBIDDEN:
        raise HTTPException(
            status_code=403,
            detail="Нет прав на изменение этого отклика",
        )
    return updated
