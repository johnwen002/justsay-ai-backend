from enum import Enum
from typing import Any, TypeVar
from uuid import UUID

from fastapi import Depends, HTTPException, status
from loguru import logger
from pydantic import BaseModel
from sqlalchemy import Select
from sqlmodel import SQLModel, asc, desc, func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.libs.db_session import get_session

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
T = TypeVar("T", bound=SQLModel)


class SortType(str, Enum):
    DESC = "desc"
    ASC = "asc"


class BaseService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
        # redis_session: redis = Depends(get_async_redis),
        # mini_client: Minio = Depends(get_minio_client),
    ):
        self.session = session
        # self.redis_session = redis_session
        # self.minio_client = mini_client

    async def search(
        self,
        *,
        model: ModelType,
        query: Select[T] | None = None,
        page: int = 0,
        page_size: int = 20,
        sort_type: SortType = None,
        sort_field: Any = None,
    ):
        """
        only works for basic query
        select(User).where(User.id="xxx")

        """
        if sort_type is not None and sort_field is None:
            raise ValueError("please set the sort_field!!")

        if sort_type is None and sort_field is not None:
            raise ValueError("please set the sort_type!!")

        if query is not None:
            stmt = query
        else:
            stmt = select(model)
        count = (
            await self.session.exec(select(func.count()).select_from(stmt.subquery()))
        ).one()

        stmt = stmt.offset(page * page_size).limit(page_size)
        if sort_type is not None and sort_field is not None:
            if sort_type == "desc":
                stmt = stmt.order_by(desc(sort_field))
            elif sort_type == "asc":
                stmt = stmt.order_by(asc(sort_field))
            else:
                raise ValueError("Only DESC or ASC works")

        db_objs = (await self.session.exec(stmt)).fetchall()
        return count, db_objs

    async def create(self, *, db_obj: ModelType):
        try:
            self.session.add(db_obj)
            await self.session.commit()
            await self.session.refresh(db_obj)
        except Exception as e:
            logger.error(f"create error: {e}")
            raise HTTPException(status_code=500, detail=f"error: {e}")

    async def update(
        self,
        *,
        id: UUID,
        obj_update: UpdateSchemaType | dict[str, Any] | ModelType,
    ):
        obj_current = await self.get(id=id)

        if not isinstance(obj_update, dict):
            obj_update = obj_update.model_dump(exclude_unset=True)

        for name, value in obj_update.items():
            if hasattr(obj_current, name):
                setattr(obj_current, name, value)

        self.session.add(obj_current)
        await self.session.commit()
        await self.session.refresh(obj_current)
        return obj_current

    async def get(self, *, model: ModelType, id: UUID):
        db_obj = await self.session.get(model, id)
        if db_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{model.__name__} not found! id={id}",
            )
        return db_obj

    async def permanent_remove(self, *, model: ModelType, id: UUID):
        db_obj = await self.get(model=model, id=id)
        logger.info(db_obj)
        if db_obj is not None:
            await self.session.delete(db_obj)
            await self.session.commit()
