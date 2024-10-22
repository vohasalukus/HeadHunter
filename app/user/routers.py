from fastapi import APIRouter
from app.user.routes.user_routers import router as user_router
from app.user.routes.resume_routers import router as resume_router


router = APIRouter(prefix="/app")

router.include_router(user_router)
router.include_router(resume_router)
