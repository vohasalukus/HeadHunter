from typing import List
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.relations.repository import SkillRepository
from app.relations.schemas import SGSkill, SCSkill, SUSkill
from app.user.dependencies import get_current_user
from app.user.models import User

router = APIRouter(
    prefix="/skills", tags=["Skills"]
)


@router.post("/", response_model=SGSkill, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)])
async def create_skill(data: SCSkill, session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    """
    Создание нового навыка
    """
    skill = await SkillRepository.create(session=session, **data.dict())
    return SGSkill.from_orm(skill)


@router.get("/", response_model=List[SGSkill])
async def get_skills(session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    """
    Получение всех навыков
    """
    skills = await SkillRepository.get_all(session=session)
    return [SGSkill.from_orm(skill) for skill in skills]


@router.put("/{skill_id}", response_model=SGSkill, dependencies=[Depends(get_current_user)])
async def update_skill(
    skill_id: int, data: SUSkill, session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)
):
    """
    Обновление навыка по ID
    """
    skill_data = data.dict(exclude_unset=True)
    skill = await SkillRepository.update(session=session, id=skill_id, data=skill_data)
    return SGSkill.from_orm(skill)


@router.delete("/{skill_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)])
async def delete_skill(skill_id: int, session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    """
    Удаление навыка по ID
    """
    await SkillRepository.destroy(session=session, id=skill_id)
    return {"message": "Successfully deleted"}