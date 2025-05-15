from datetime import datetime

import httpx
from loguru import logger
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import settings
from src.models.follow import FollowRSSPath
from src.models.rss import RSSInfomation


async def get_rss(url: str):
    async with httpx.AsyncClient() as client:
        from email.utils import parsedate_to_datetime

        infomation_xml = await client.get(url)
        import xml.etree.ElementTree as ET

        root = ET.fromstring(infomation_xml)
        items = root.findall("item")
        return [
            {
                "title": item.find("title").text,
                "description": item.find("description").text,
                "link": item.find("link").text if item.find("link") else None,
                "guid": item.find("guid").text if item.find("guid") else None,
                "pubDate": (
                    parsedate_to_datetime(item.find("pubDate").text)
                    if item.find("pubDate")
                    else datetime.now()
                ),
                "author": item.find("author").text if item.find("author") else None,
            }
            for item in items
        ]


async def get_rss_schedule(session: AsyncSession):
    stmt = select(FollowRSSPath.rss_path).distinct()
    follow_rss_path_list = (await session.exec(stmt)).fetchall()
    if not follow_rss_path_list:
        logger.info("rss follow not found. ")

    results = []
    for rss_path in follow_rss_path_list:
        result = await get_rss(f"${settings.RSSHUB_URL}{rss_path}")
        results.append(result)

    stmt = (
        insert(RSSInfomation)
        .values(results)
        .on_conflict_do_nothing(constraint=[RSSInfomation.title])
    )

    await session.exec(stmt)
