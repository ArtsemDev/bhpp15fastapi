from fastapi import APIRouter
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from api.annotated_types import CategoryID
from src.types import CategoryCreateDTO, CategoryDTO, CategoryUpdateDTO

router = APIRouter(tags=["Category"])


@router.get(
    path="/categories",
    response_model=list[CategoryDTO],
    status_code=HTTP_200_OK,
    response_description="List of categories",
    summary="Getting a list of categories",
    name="category-list"
)
async def category_list():
    return [CategoryDTO(id=1, name="Sport"), CategoryDTO(id=2, name="Finance")]


@router.post(
    path="/categories",
    response_model=CategoryDTO,
    status_code=HTTP_201_CREATED,
    response_description="Detail of category",
    summary="Creating a new category",
    name="category-create"
)
async def category_create(data: CategoryCreateDTO):
    return CategoryDTO(id=3, **data.model_dump())


@router.get(
    path="/categories/{id}",
    response_model=CategoryDTO,
    status_code=HTTP_200_OK,
    name="category-detail"
)
async def category_detail(pk: CategoryID):
    return CategoryDTO(id=pk, name="Mock")


@router.put(
    path="/categories/{id}",
    status_code=HTTP_201_CREATED,
    response_model=CategoryDTO,
    name="category-update"
)
async def category_update(body: CategoryUpdateDTO, pk: CategoryID):
    return CategoryDTO(id=pk, **body.model_dump())


@router.delete(
    path="/categories/{id}",
    status_code=HTTP_204_NO_CONTENT,
    name="category-delete"
)
async def category_delete(pk: CategoryID):
    return
