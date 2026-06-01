from datetime import datetime, timezone

from sqlmodel import SQLModel, Field


class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: int | None = Field(default=None, primary_key=True)

    name: str = Field(index=True, min_length=1, max_length=100)
    slug: str = Field(index=True, unique=True, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=500)

    is_active: bool = Field(default=True)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
