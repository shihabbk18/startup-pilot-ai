from fastapi import APIRouter

from app.api.v1 import auth, documents, generations, health, projects

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(generations.router, tags=["generations"])
api_router.include_router(documents.router, tags=["documents"])

