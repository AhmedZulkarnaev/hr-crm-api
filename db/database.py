"""Подключение к БД и фабрика сессий SQLAlchemy."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

SQLALCHEMY_DATABASE_URL = (
    "postgresql+psycopg://postgres:admin@localhost:5432/hr_crm"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Выдаёт сессию БД для запроса; закрывает её после обработки."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
