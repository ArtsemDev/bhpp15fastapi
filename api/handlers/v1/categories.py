from fastapi import APIRouter, HTTPException
from sqlalchemy import select, asc, desc, delete, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from api.annotated_types import CategoryID, PageQuery, PageNumberQuery, CategorySortAttrQuery, SortByQuery
from src.database import Category, Article
from src.dependencies.authenticate import authenticate
from src.dependencies.database_session import DBAsyncSession
from src.types import CategoryCreateDTO, CategoryDTO, CategoryUpdateDTO, CategoryExtendedDTO

router = APIRouter(tags=["Category"])


@router.get(
    path="/categories",
    response_model=list[CategoryDTO],
    status_code=HTTP_200_OK,
    response_description="List of categories",
    summary="Getting a list of categories",
    name="category-list"
)
async def category_list(
        session: DBAsyncSession,
        page: PageQuery = 1,
        page_number: PageNumberQuery = 25,
        order: CategorySortAttrQuery = "id",
        order_by: SortByQuery = "asc"
):
    statement = select(Category).limit(page_number).offset(page * page_number - page_number)

    if order_by == "asc":
        statement = statement.order_by(asc(order))
    else:
        statement = statement.order_by(desc(order))

    objs = await session.scalars(statement=statement)
    return [CategoryDTO.model_validate(obj=obj) for obj in objs.all()]


# @router.get(path="/job")
# async def start_job():
#     task = foo.delay(6, 6)
#     return {"job_id": task.id}
#
#
# @router.get(path="/job/status/{job_id}")
# async def get_job(job_id: str = Path()):
#     task = AsyncResult(id=job_id)
#     return {"status": task.status}


@router.post(
    path="/categories",
    response_model=CategoryDTO,
    status_code=HTTP_201_CREATED,
    response_description="Detail of category",
    summary="Creating a new category",
    dependencies=[authenticate],
    name="category-create"
)
async def category_create(session: DBAsyncSession, data: CategoryCreateDTO):
    category = Category(**data.model_dump())
    session.add(instance=category)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"category {data.name} exists")
    else:
        await session.refresh(instance=category)
        return CategoryDTO.model_validate(obj=category)


@router.get(
    path="/categories/{id}",
    response_model=CategoryExtendedDTO,
    status_code=HTTP_200_OK,
    name="category-detail"
)
async def category_detail(session: DBAsyncSession, pk: CategoryID):
    category = await session.scalar(
        statement=select(Category)
        .options(
            joinedload(Category.articles).subqueryload(Article.tags),
        )
        .filter(and_(Category.id == pk))
    )
    if category is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"category {pk} does not exist")
    return CategoryExtendedDTO.model_validate(obj=category)


@router.put(
    path="/categories/{id}",
    status_code=HTTP_201_CREATED,
    response_model=CategoryDTO,
    dependencies=[authenticate],
    name="category-update"
)
async def category_update(session: DBAsyncSession, body: CategoryUpdateDTO, pk: CategoryID):
    obj = await session.get(entity=Category, ident=pk)
    for k, v in body:
        setattr(obj, k, v)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="category name is not unique")
    else:
        return CategoryDTO.model_validate(obj=obj)


@router.delete(
    path="/categories/{id}",
    status_code=HTTP_204_NO_CONTENT,
    dependencies=[authenticate],
    name="category-delete",
)
async def category_delete(session: DBAsyncSession, pk: CategoryID):
    await session.execute(delete(Category).filter(and_(Category.id == pk)))
    await session.commit()
