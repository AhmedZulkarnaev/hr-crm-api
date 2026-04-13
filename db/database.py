"""Подключение к БД и фабрика сессий SQLAlchemy."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from core.constants import SQLITE_DB_URL

engine = create_engine(
    SQLITE_DB_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Выдаёт сессию БД для запроса; закрывает её после обработки."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
