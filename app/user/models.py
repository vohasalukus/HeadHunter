from enum import Enum as PyEnum
from typing import List

from sqlalchemy import String, Enum, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from app.database import Base
# from app.relations.relations_application import Application
# from app.relations.relations_skill import Skill


class UserRole(PyEnum):
    ADMIN = 'admin'
    JOBSEEKER = 'jobseeker'
    RECRUITER = 'recruiter'

class User(Base):

    name: Mapped[str] = mapped_column(String(256), index=True)
    email: Mapped[str] = mapped_column(String(256), index=True)
    hashed_password: Mapped[str] = mapped_column(String(256))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole))

    # One to many
    resumes: Mapped[List["Resume"]] = relationship("Resume", back_populates="user")

    # One to many
    applications: Mapped[List["Application"]] = relationship("Application", back_populates="user")


class Resume(Base):

    name: Mapped[str] = mapped_column(String(256), index=True)
    desired_salary: Mapped[int] = mapped_column(Integer)
    profession: Mapped[str] = mapped_column(String(256), index=True)

    # One to many - у одно юзера может быть много резюме
    user: Mapped[User] = relationship("User", back_populates="resumes")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))

    # Many to many - связь со скиллами

    skills: Mapped[List["Skill"]] = relationship(
        secondary="resume_skill", back_populates="resumes"
    )

