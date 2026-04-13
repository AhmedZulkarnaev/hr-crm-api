"""Пакет ORM-моделей приложения."""

from .applications import Application
from .users import User
from .vacancies import Vacancy

__all__ = ["Application", "User", "Vacancy"]
