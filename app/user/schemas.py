from typing import List

from pydantic import BaseModel

from app.relations.schemas import SSkill
from app.user.models import UserRole


class SUser(BaseModel):
    name: str
    email: str
    hashed_password: str
    role: UserRole

    resumes: List
    applications: List


class SResume(BaseModel):

    name: str
    desired_salary: int
    profession: str

    user_id: int

    skills: List["SSkill"]
