from fastapi import APIRouter

from src.routes import avikus

api_router = APIRouter()

api_router.include_router(
    avikus.route,
    tags=['avikus']
)
