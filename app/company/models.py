from datetime import datetime
from typing import List

from sqlalchemy import String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from app.database import Base


class Company(Base):

    name: Mapped[str] = mapped_column(String(256), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # One to many
    vacancies: Mapped[List["Vacancy"]] = relationship("Vacancy", back_populates="company")

    # One to many
    applications: Mapped[List["Application"]] = relationship("Application", back_populates="company")


class Vacancy(Base):

    name: Mapped[str] = mapped_column(String(256), index=True)
    salary: Mapped[int] = mapped_column(Integer)
    req_experience: Mapped[str] = mapped_column(String(256))
    schedule: Mapped[str] = mapped_column(String(256))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)

    # Many to one - у одной компании много вакансии
    company: Mapped[Company] = relationship("Company", back_populates="vacancies")
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("companies.id"))

    # Many to many - со скиллами

    skills: Mapped[List["Skill"]] = relationship(
        secondary="vacancy_skill", back_populates="vacancies"
    )
