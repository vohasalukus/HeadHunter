from app.relations.relations_application import Application
from app.relations.relations_skill import Skill
from app.repository.base import BaseRepository


class SkillRepository(BaseRepository):
    model = Skill


class ApplicationRepository(BaseRepository):
    model = Application
