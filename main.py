from fastapi import FastAPI

from api.users import router as users_router
from api.vacancies import router as vacancies_router
from api.applications import router as applications_router


app = FastAPI(
    title="HR CRM API",
    description="Мощная система для найма сотрудников 🚀",
    version="1.0.0"
)

app.include_router(users_router)
app.include_router(vacancies_router)
app.include_router(applications_router)
