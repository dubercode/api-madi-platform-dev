from fastapi import APIRouter

from app.api.v1.endpoints import diseases, health


api_router = APIRouter()

api_router.include_router(
    health.router,
    prefix="/health",
)

api_router.include_router(
    diseases.router,
)