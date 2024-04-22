from pydantic import Field, PositiveInt

from .articles import ArticleDTO
from .base import DTO


class CategoryCreateDTO(DTO):
    name: str = Field(
        min_length=2,
        max_length=64,
    )


class CategoryUpdateDTO(CategoryCreateDTO):
    ...


class CategoryDTO(CategoryCreateDTO):
    id: PositiveInt


class CategoryExtendedDTO(CategoryDTO):
    articles: list[ArticleDTO]
