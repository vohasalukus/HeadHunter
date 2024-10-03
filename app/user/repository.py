from app.repository.base import BaseRepository
from app.user.models import User, Resume


class UserRepository(BaseRepository):
    model = User


class ResumeRepository(BaseRepository):
    model = Resume
