from fastapi import APIRouter

from src.rss.schema import FollowRSSPathSchema

api = APIRouter()


@api.get("/follow-rss")
async def filter(schema: FollowRSSPathSchema):
    pass
