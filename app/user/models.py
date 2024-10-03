import enum as PyEnum
from typing import List

from sqlalchemy import String, Enum, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from app.database import Base


class UserRole(PyEnum):
    ADMIN = 'admin'
    jobseeker = 'jobseeker'
    recruiter = 'recruiter'

class User(Base):

    name: Mapped[str] = mapped_column(String(256), index=True)
    email: Mapped[str] = mapped_column(String(256), index=True)
    hashed_password: Mapped[str] = mapped_column(String(256))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole))

    resumes: Mapped[List["Resume"]] = relationship("Resume", back_populates="user")

class Resume(Base):

    name: Mapped[str] = mapped_column(String(256), index=True)
    desired_salary: Mapped[int] = mapped_column(Integer)
    profession: Mapped[str] = mapped_column(String(256), index=True)

    # One to many - у одно юзера может быть много резюме
    user: Mapped[User] = relationship("User", back_populates="resumes")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))

