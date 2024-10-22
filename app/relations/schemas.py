from typing import List

from pydantic import BaseModel


# Application Schemas
class SGApplication(BaseModel):
    id: int
    status: str
    letter: str
    user_id: int
    company_id: int


class SUApplication(BaseModel):
    status: str | None = None
    letter: str | None = None


class SRApplication(BaseModel):
    status: str
    letter: str


class SCApplication(BaseModel):
    status: str
    letter: str
    user_id: int
    company_id: int


# Skills Schemas
class SGSkill(BaseModel):
    id: int
    name: str
    experience: str

    class Config:
        from_attributes = True


class SUSkill(BaseModel):
    name: str | None = None
    experience: str | None = None


class SRSkill(BaseModel):
    name: str
    experience: str


class SCSkill(BaseModel):
    name: str
    experience: str
