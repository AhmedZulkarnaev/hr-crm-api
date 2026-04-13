"""Сервисная логика откликов на вакансии."""

from sqlalchemy.orm import Session

from core.constants import APPLICATION_NOT_FOUND, FORBIDDEN, VACANCY_NOT_FOUND
from models.applications import Application
from models.vacancies import Vacancy
from schemas.applications import ApplicationCreate


def create_application(
    db: Session,
    application: ApplicationCreate,
    current_user: int,
) -> Application | None:
    """Создаёт отклик кандидата и сохраняет в БД."""
    vacancy = db.get(Vacancy, application.vacancy_id)

    if not vacancy:
        return None

    db_application = Application(
        **application.model_dump(),
        candidate_id=current_user,
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application


def update_application_status_service(
    db: Session,
    application_id: int,
    new_status: str,
    hr_id: int,
) -> tuple[Application | None, str | None]:
    """Меняет статус отклика для вакансии, которой владеет указанный HR."""
    application = db.get(Application, application_id)
    if not application:
        return None, APPLICATION_NOT_FOUND

    vacancy = db.get(Vacancy, application.vacancy_id)
    if not vacancy:
        return None, VACANCY_NOT_FOUND

    if vacancy.hr_id != hr_id:
        return None, FORBIDDEN

    application.status = new_status
    db.commit()
    db.refresh(application)
    return application, None
