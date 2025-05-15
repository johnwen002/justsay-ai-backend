from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlmodel.ext.asyncio.session import AsyncSession

from src.events.rss import get_rss_schedule

scheduler: AsyncIOScheduler = AsyncIOScheduler()


async def initialize(session: AsyncSession):
    scheduler.add_job(
        func=get_rss_schedule, args=(session,), trigger=CronTrigger(hour=1)
    )
    scheduler.start()
