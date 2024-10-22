from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.user.dependencies import get_current_user
from app.user.models import User, Resume
from app.user.repository import ResumeRepository
from app.user.schemas import SGResume, SCResume, SUResume

router = APIRouter(
    prefix="/resume",
    tags=["Resumes"],
)


@router.post("/", response_model=SGResume, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)])
async def create_resume(data: SCResume, session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    """
    Создание нового резюме текущего пользователя
    """
    resume_data = data.dict()
    resume_data["user_id"] = current_user.id
    resume = await ResumeRepository.create(session=session, **resume_data)
    return SGResume.from_orm(resume)


@router.get("/", response_model=List[SGResume])
async def get_resumes(session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    """
    Получение всех резюме текущего пользователя
    """
    resumes = await ResumeRepository.filter(session=session, user_id=current_user.id, includes=["skills"])
    return [SGResume.from_orm(resume) for resume in resumes]


@router.put("/{resume_id}", response_model=SGResume, dependencies=[Depends(get_current_user)])
async def update_resume(
        resume_id: int, data: SUResume, session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    """
    Обновление резюме по ID текущего пользователя
    """

    resumes = await ResumeRepository.filter(session=session, id=resume_id, user_id=current_user.id, includes=["skills"])
    if not resumes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Resume not found or you do not have permission to update it")

    resume = resumes[0]


    resume_data = data.dict(exclude_unset=True)
    updated_resume = await ResumeRepository.update(session=session, id=resume.id, data=resume_data)

    return SGResume.from_orm(updated_resume)


@router.delete("/{resume_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)])
async def delete_resume(resume_id: int, session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    """
    Удаление резюме текущего пользователя по ID
    """
    resume = await ResumeRepository.filter(session=session, user_id=current_user.id, includes=["skills"])

    try:
        await ResumeRepository.destroy(session=session, id=resume_id)
    except TypeError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found or you do not have permission to delete it")

    return {"message": "Successfully deleted"}
