from fastapi import FastAPI
from app.user.routers import router as user_router
from app.relations.routers import router as relation_router

app = FastAPI()

app.include_router(user_router)
app.include_router(relation_router)
