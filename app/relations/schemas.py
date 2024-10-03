from typing import List

from pydantic import BaseModel

from app.company.schemas import SVacancy
from app.relations.relations_application import StatusApplication
from app.user.schemas import SResume


class SSkill(BaseModel):
    name: str
    experience: str

    resumes: List["SResume"]
    vacancies: List["SVacancy"]


class SApplication(BaseModel):
    status: StatusApplication
    letter: str

    user_id: int
    company_id: int

