from datetime import datetime
from typing import List

from pydantic import BaseModel


# Company Schemas
class SGCompany(BaseModel):
    id: int
    name: str
    description: str | None = None


class SUCompany(BaseModel):
    name: str | None = None
    description: str | None = None


class SRCompany(BaseModel):
    name: str
    description: str | None = None


class SCCompany(BaseModel):
    name: str
    description: str | None = None


# Vacancy Schemas
class SGVacancy(BaseModel):
    id: int
    name: str
    salary: int
    req_experience: str
    schedule: str
    description: str | None = None
    company_id: int
    skills: List['SGSkill'] = []
    created_at: datetime


class SUVacancy(BaseModel):
    name: str | None = None
    salary: int | None = None
    req_experience: str | None = None
    schedule: str | None = None
    description: str | None = None
    skills: List['SGSkill'] | None = None


class SRVacancy(BaseModel):
    name: str
    salary: int
    req_experience: str
    schedule: str
    description: str | None = None
    skills: List['SGSkill'] = []
    created_at: datetime


class SCVacancy(BaseModel):
    name: str
    salary: int
    req_experience: str
    schedule: str
    description: str | None = None
    company_id: int
    skills: List['SGSkill'] = []
    created_at: datetime
