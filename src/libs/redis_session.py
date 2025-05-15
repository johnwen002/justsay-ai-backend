import redis.asyncio as redis
from fastapi import Query

from src.config import settings


async def get_async_client():
    client = redis.Redis.from_url(str(settings.REDIS_URI))
    return client


async def get_async_redis(
    auto_close: bool = Query(default=True, include_in_schema=False)
):
    client = None
    try:
        client = await get_async_client()
        yield client
    finally:
        if auto_close:
            await client.aclose()