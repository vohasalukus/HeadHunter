from typing import List

from sqlalchemy import String, Table, Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

# from app.company.models import Vacancy
from app.database import Base
# from app.user.models import Resume


class Skill(Base):

    name: Mapped[str] = mapped_column(String(256), index=True)
    experience: Mapped[str] = mapped_column(String(256), index=True)

    resumes: Mapped[List["Resume"]] = relationship(
        secondary="resume_skill", back_populates="skills"
    )

    vacancies: Mapped[List["Vacancy"]] = relationship(
        secondary="vacancy_skill", back_populates="skills"
    )

resume_skill = Table(
    "resume_skill",
    Base.metadata,
    Column("resume_id", Integer, ForeignKey("resumes.id"), primary_key=True),
    Column("skill_id", Integer, ForeignKey("skills.id"), primary_key=True)
)

vacancy_skill = Table(
    "vacancy_skill",
    Base.metadata,
    Column("vacancy_id", Integer, ForeignKey("vacancies.id"), primary_key=True),
    Column("skill_id", Integer, ForeignKey("skills.id"), primary_key=True)
)
