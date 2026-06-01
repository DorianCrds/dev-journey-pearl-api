class CategoryNotFoundError(Exception):
    def __init__(self, identifier: int | str, lookup_field: str = "id") -> None:
        self.identifier = identifier
        self.lookup_field = lookup_field
        super().__init__(
            f"Category with {lookup_field} '{identifier}' was not found."
        )


class CategorySlugAlreadyExistsError(Exception):
    def __init__(self, slug: str) -> None:
        self.slug = slug
        super().__init__(f"Category with slug '{slug}' already exists.")
