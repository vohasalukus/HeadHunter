from enum import Enum as PyEnum

from sqlalchemy import Enum, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from app.company.models import Company
from app.database import Base
# from app.user.models import User


class StatusApplication(PyEnum):
    NEW = "new"
    OLD = "old"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Application(Base):
    status: Mapped[StatusApplication] = mapped_column(Enum(StatusApplication))
    letter: Mapped[str] = mapped_column(Text)\

    # One to many - с юзерами, много откликов, но может все одни принадлежат одному юзеру

    user: Mapped["User"] = relationship("User", back_populates="applications")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    # One to many - с компаниями, много откликов, но все принадлежат одной компании

    company: Mapped["Company"] = relationship("Company", back_populates="applications")
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("companies.id"))
