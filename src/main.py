import contextlib

from fastapi import FastAPI
from loguru import logger
from sqlmodel.ext.asyncio.session import AsyncSession

from src.events.rss import get_rss_schedule
from src.libs.db_session import get_session
from src.tasks.scheduler import initialize


@contextlib.asynccontextmanager
async def lifepan(app: FastAPI):
    """
    start job
    """
    logger.info("===== app start ====")
    session: AsyncSession = None
    try:
        session = await anext(get_session(False))
        await initialize(session)  # 创建任务
        await get_rss_schedule(session)  # 应用启动立即执行任务

    except Exception as e:
        logger.error(f"start application error: {e}")
    finally:
        if session is not None:
            await session.aclose()
    yield
    logger.info("==== app shutdown =====")


app = FastAPI(lifespan=lifepan)


from src.routes import *  # noqa
