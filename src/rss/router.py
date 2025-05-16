from typing import Annotated

from fastapi import APIRouter, Depends

from src.rss.schema import FollowRSSPathSchema
from src.rss.services import RSSService

api = APIRouter()


@api.get("/rss")
async def rss(
    rss_path: str,
    service: Annotated[RSSService, Depends()],
):
    count, rss = await service.get_rss(rss_path=rss_path)
    return {"total": count, "rss": rss}


@api.get("/follow-rss")
async def filter(
    category: str,
    service: Annotated[RSSService, Depends()],
    page: int = 0,
    page_size=10,
):
    count, results = await service.filter(
        category=category.upper(), page=page, page_size=page_size
    )
    return {"total": count, "results": results}


@api.post("/create-follow-rss")
async def follow(
    schema: FollowRSSPathSchema, service: Annotated[RSSService, Depends()]
):
    await service.add(schema=schema)


@api.post("/batch-create-follow-rss")
async def batch_follow(
    schemas: list[FollowRSSPathSchema], service: Annotated[RSSService, Depends()]
):
    await service.batch_create(schemas=schemas)


@api.delete("/remove-follow-rss")
async def remove(id: str, service: Annotated[RSSService, Depends()]):
    await service.remove(id=id)
