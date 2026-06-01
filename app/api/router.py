from fastapi import APIRouter

from app.modules.categories.router import admin_router as categories_admin_router
from app.modules.categories.router import router as categories_router


api_router = APIRouter()


@api_router.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


api_router.include_router(categories_router)
api_router.include_router(categories_admin_router)