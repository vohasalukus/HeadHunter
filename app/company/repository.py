from app.company.models import Company, Vacancy
from app.repository.base import BaseRepository


class CompanyRepository(BaseRepository):
    model = Company


class VacancyRepository(BaseRepository):
    model = Vacancy
