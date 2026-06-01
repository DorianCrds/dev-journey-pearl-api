# Import all SQLModel models here so SQLModel can detect them
# when creating database tables.

from sqlmodel import SQLModel  # noqa: F401

from app.modules.categories.models import Category  # noqa: F401