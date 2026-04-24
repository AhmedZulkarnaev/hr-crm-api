from pydantic import BaseModel, ConfigDict


class CandidateProfileCreate(BaseModel):
    """Данные для создания профиля кандидата."""
    cv_url: str | None = None


class CandidateProfileResponse(BaseModel):
    """То, что мы отдаем на фронтенд."""
    id: int
    user_id: int
    cv_url: str | None

    model_config = ConfigDict(from_attributes=True)


class HRProfileCreate(BaseModel):
    """Данные для создания профиля HR."""
    company_name: str


class HRProfileResponse(BaseModel):
    """То, что мы отдаем на фронтенд."""
    id: int
    user_id: int
    company_name: str

    model_config = ConfigDict(from_attributes=True)
