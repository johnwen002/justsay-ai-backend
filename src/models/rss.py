from datetime import datetime
from pydantic import Field

from src.models.base import BaseSQLModel


class RSSInfomation(BaseSQLModel, table=True):
    __tablename__ = "rss"
    title: str = Field(nullable=False, unique=True)
    description: str = Field(nullable=True)
    link: str = Field(nullable=True)
    guid: str = Field(nullable=True)
    pub_date: datetime = Field(nullable=True)
    author: str = Field(nullable=True)
    rss_path: str = Field(nullable=False)
