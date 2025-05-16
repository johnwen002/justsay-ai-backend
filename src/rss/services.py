from datetime import date, datetime, time

from sqlalchemy.dialects.postgresql import insert
from sqlmodel import and_, select

from src.models.follow import FollowRSSPath
from src.models.rss import RSSInfomation
from src.rss.schema import FollowRSSPathSchema
from src.service import BaseService


class RSSService(BaseService):
    async def get_rss(self, *, rss_path: str):
        today_date: date = date.today()  # 1. 获取今天的日期

        return await self.search(
            model=RSSInfomation,
            query=select(RSSInfomation).where(
                and_(
                    RSSInfomation.rss_path == rss_path,
                    RSSInfomation.pub_date >= datetime.combine(today_date, time.min),
                    RSSInfomation.pub_date <= datetime.combine(today_date, time.max),
                )
            ),
        )

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
