from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.catalogs import router as catalogs_router
from app.api.v1.segments import router as segments_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(catalogs_router)
api_router.include_router(segments_router)
