from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.db.session import get_session
from app.modules.categories.exceptions import (
    CategoryNotFoundError,
    CategorySlugAlreadyExistsError,
)
from app.modules.categories.repository import CategoryRepository
from app.modules.categories.schemas import CategoryCreate, CategoryRead, CategoryUpdate
from app.modules.categories.service import CategoryService


router = APIRouter(tags=["Categories"])
admin_router = APIRouter(prefix="/admin/categories", tags=["Admin - Categories"])


def get_category_service(session: Session = Depends(get_session)) -> CategoryService:
    repository = CategoryRepository(session)
    return CategoryService(repository)


@router.get("/categories", response_model=list[CategoryRead])
def list_categories(
    service: CategoryService = Depends(get_category_service),
) -> list[CategoryRead]:
    return service.list_public_categories()


@router.get("/categories/{category_slug}", response_model=CategoryRead)
def get_category(
    category_slug: str,
    service: CategoryService = Depends(get_category_service),
) -> CategoryRead:
    try:
        return service.get_public_category(category_slug)
    except CategoryNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@admin_router.get("", response_model=list[CategoryRead])
def list_admin_categories(
    service: CategoryService = Depends(get_category_service),
) -> list[CategoryRead]:
    return service.list_admin_categories()


@admin_router.get("/{category_id}", response_model=CategoryRead)
def get_admin_category(
    category_id: int,
    service: CategoryService = Depends(get_category_service),
) -> CategoryRead:
    try:
        return service.get_category(category_id)
    except CategoryNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@admin_router.post(
    "",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    data: CategoryCreate,
    service: CategoryService = Depends(get_category_service),
) -> CategoryRead:
    try:
        return service.create_category(data)
    except CategorySlugAlreadyExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@admin_router.patch("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    service: CategoryService = Depends(get_category_service),
) -> CategoryRead:
    try:
        return service.update_category(category_id, data)
    except CategoryNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    except CategorySlugAlreadyExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@admin_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    service: CategoryService = Depends(get_category_service),
) -> None:
    try:
        service.delete_category(category_id)
    except CategoryNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
