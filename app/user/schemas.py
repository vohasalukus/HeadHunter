from typing import List

from pydantic import BaseModel, EmailStr

from app.user.models import UserRole


# User Schemas
class SGUser(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole


class SUUser(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    role: UserRole | None = None


class SAuth(BaseModel):
    email: EmailStr
    password: str


class SRUser(BaseModel):
    name: str
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True


class SCUser(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole


# Resume Schemas
class SGResume(BaseModel):
    id: int
    name: str
    desired_salary: int
    profession: str
    user_id: int
    skills: List['SGSkill'] = []


class SUResume(BaseModel):
    name: str | None = None
    desired_salary: int | None = None
    profession: str | None = None
    skills: List['SGSkill'] | None = None


class SRResume(BaseModel):
    name: str
    desired_salary: int
    profession: str
    skills: List['SGSkill'] = []


class SCResume(BaseModel):
    name: str
    desired_salary: int
    profession: str
    user_id: int
    skills: List['SGSkill'] = []
