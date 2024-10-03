from datetime import datetime
from typing import List

from sqlalchemy import String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from app.database import Base
from app.relations.relations_skill import Skill


class Company(Base):

    name: Mapped[str] = mapped_column(String(256), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # One to many
    vacancies: Mapped[List["Company"]] = relationship("Vacancy", back_populates="company")

class Vacancy(Base):

    name: Mapped[str] = mapped_column(String(256), index=True)
    salary: Mapped[int] = mapped_column(Integer)
    req_experience: Mapped[str] = mapped_column(String(256))
    schedule: Mapped[str] = mapped_column(String(256))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)

    # One to many - у одной компании много вакансии
    company: Mapped[Company] = relationship("Company", back_populates="vacancies")
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("company.id"))

    # Many to many - со скиллами

    skills: Mapped[List["Skill"]] = relationship(
        secondary="vacancy_skill", back_populates="vacancies"
    )