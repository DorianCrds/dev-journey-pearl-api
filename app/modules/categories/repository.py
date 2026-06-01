from sqlmodel import Session, select

from app.modules.categories.models import Category


class CategoryRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_active(self) -> list[Category]:
        statement = (
            select(Category)
            .where(Category.is_active == True)  # noqa: E712
            .order_by(Category.name)
        )
        return list(self.session.exec(statement).all())

    def list_all(self) -> list[Category]:
        statement = select(Category).order_by(Category.name)
        return list(self.session.exec(statement).all())

    def get_by_id(self, category_id: int) -> Category | None:
        return self.session.get(Category, category_id)

    def get_active_by_slug(self, slug: str) -> Category | None:
        statement = select(Category).where(
            Category.slug == slug,
            Category.is_active == True,  # noqa: E712
        )
        return self.session.exec(statement).first()

    def get_by_slug(self, slug: str) -> Category | None:
        statement = select(Category).where(Category.slug == slug)
        return self.session.exec(statement).first()

    def create(self, category: Category) -> Category:
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category

    def update(self, category: Category) -> Category:
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category
