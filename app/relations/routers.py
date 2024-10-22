from fastapi import APIRouter
from app.relations.routes.skill_routers import router as skill_router
from app.relations.routes.application_routers import router as application_router


router = APIRouter(prefix="/app")

router.include_router(skill_router)
router.include_router(application_router)
