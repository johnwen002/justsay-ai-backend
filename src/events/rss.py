import asyncio
import datetime

import httpx
from loguru import logger
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import settings
from src.models.follow import FollowRSSPath
from src.models.rss import RSSInfomation


def convert_http_date_to_datetime_strptime(date_string: str) -> datetime:
    """
    使用 strptime 将 "Wed, 14 May 2025 04:33:04 GMT" 格式的字符串
    转换为一个时区感知的 Python datetime 对象 (UTC)。

    参数:
        date_string (str): 要转换的日期字符串。

    返回:
        datetime: 一个表示相同日期和时间的时区感知的 datetime 对象，时区为 UTC。
    """
    # "%a" - 星期几的缩写
    # "%d" - 月份中的日期 (01-31)
    # "%b" - 月份的缩写
    # "%Y" - 四位数的年份
    # "%H" - 24小时制的小时 (00-23)
    # "%M" - 分钟 (00-59)
    # "%S" - 秒 (00-59)
    # "GMT" - 字面量匹配 "GMT"
    format_string = "%a, %d %b %Y %H:%M:%S GMT"

    # strptime 解析后得到一个 naive datetime 对象 (没有时区信息)
    naive_dt_object = datetime.datetime.strptime(date_string, format_string)

    # 将 naive datetime 对象转换为 aware datetime 对象，并设置时区为 UTC

    return naive_dt_object


async def get_rss(path: str):
    async with httpx.AsyncClient() as client:
        # from email.utils import parsedate_to_datetime

        infomation_xml = await client.get(f"{settings.RSSHUB_URL}{path}")
        import xml.etree.ElementTree as ET

        root = ET.fromstring(infomation_xml.text)
        channel = root.find("channel")
        if channel is None:
            return []

        items = channel.findall("item")
        return [
            {
                "title": item.find("title").text,
                "description": item.find("description").text,
                "link": item.find("link").text,
                "guid": item.find("guid").text,
                "pub_date": convert_http_date_to_datetime_strptime(
                    item.find("pubDate").text
                ),
                "author": item.find("author").text,
                "rss_path": path,
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
        result = await get_rss(rss_path)
        results.extend(result)
        if "twiiter" in rss_path:
            await asyncio.sleep(10)
    logger.info(results)
    stmt = (
        insert(RSSInfomation)
        .values(results)
        .on_conflict_do_nothing(index_elements=["title"])
    )

    await session.exec(stmt)
    await session.commit()
