from sqlalchemy.dialects.postgresql import insert
from sqlmodel import select

from src.models.follow import FollowRSSPath
from src.rss.schema import FollowRSSPathSchema
from src.service import BaseService


class RSSService(BaseService):
    async def add(self, *, schema: FollowRSSPathSchema):
        await self.create(db_obj=FollowRSSPath(**schema.model_dump()))

    async def batch_create(self, *, schemas: list[FollowRSSPathSchema]):
        values = [schema.model_dump() for schema in schemas]
        stmt = insert(FollowRSSPath).values(values)
        await self.session.exec(stmt)
        await self.session.commit()

    async def filter(self, *, category: str, page: int, page_size: int):
        return await self.search(
            model=FollowRSSPath,
            query=select(FollowRSSPath).where(FollowRSSPath.category_name == category),
            page=page,
            page_size=page_size,
        )

    async def remove(self, *, id: str):
        await self.remove(id=id)
