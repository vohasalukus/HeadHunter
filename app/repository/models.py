from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from app.database import Base


class Skill(Base):

    name: Mapped[str] = mapped_column(String(256), index=True)
    experience: Mapped[str] = mapped_column(String(256), index=True)


