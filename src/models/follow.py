from pydantic import Field

from src.models.base import BaseSQLModel


class FollowRSSPath(BaseSQLModel, table=True):
    __tablename__ = "follow_rss_path"
    user_id: str = Field(nullable=True)
    rss_path: str = Field(nullable=True)
