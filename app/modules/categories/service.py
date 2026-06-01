from datetime import datetime, timezone

from app.modules.categories.exceptions import (
    CategoryNotFoundError,
    CategorySlugAlreadyExistsError,
)
from app.modules.categories.models import Category
from app.modules.categories.repository import CategoryRepository
from app.modules.categories.schemas import CategoryCreate, CategoryUpdate


class CategoryService:
    def __init__(self, repository: CategoryRepository) -> None:
        self.repository = repository

    def list_public_categories(self) -> list[Category]:
        return self.repository.list_active()

    def list_admin_categories(self) -> list[Category]:
        return self.repository.list_all()

    def get_public_category(self, slug: str) -> Category:
        category = self.repository.get_active_by_slug(slug)

        if category is None:
            raise CategoryNotFoundError(slug, lookup_field="slug")

        return category

    def get_category(self, category_id: int) -> Category:
        category = self.repository.get_by_id(category_id)

        if category is None:
            raise CategoryNotFoundError(category_id)

        return category

    def create_category(self, data: CategoryCreate) -> Category:
        existing_category = self.repository.get_by_slug(data.slug)

        if existing_category is not None:
            raise CategorySlugAlreadyExistsError(data.slug)

        category = Category(
            name=data.name,
            slug=data.slug,
            description=data.description,
        )

        return self.repository.create(category)

    def update_category(self, category_id: int, data: CategoryUpdate) -> Category:
        category = self.repository.get_by_id(category_id)

        if category is None:
            raise CategoryNotFoundError(category_id)

        if data.slug is not None and data.slug != category.slug:
            existing_category = self.repository.get_by_slug(data.slug)

            if existing_category is not None:
                raise CategorySlugAlreadyExistsError(data.slug)

        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return category

        for field_name, value in update_data.items():
            setattr(category, field_name, value)

        category.updated_at = datetime.now(timezone.utc)

        return self.repository.update(category)

    def delete_category(self, category_id: int) -> None:
        category = self.repository.get_by_id(category_id)

        if category is None:
            raise CategoryNotFoundError(category_id)

        if category.is_active:
            category.is_active = False
            category.updated_at = datetime.now(timezone.utc)
            self.repository.update(category)
