from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.relations.schemas import SSkill


class Company(BaseModel):
    name: str
    description: str | None

    vacancies: List
    applications: List


class SVacancy(BaseModel):
    name: str
    salary: int
    req_experience: str
    schedule: str
    description: str | None
    created_at: datetime

    company_id: int

    skills: List["SSkill"]

