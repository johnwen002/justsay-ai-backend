from pydantic import BaseModel, Field


class FollowRSSPathSchema(BaseModel):
    user_id: str = Field(..., description="user id")
    rss_path: str = Field(..., description="rss_path")
    category_name: str = Field(..., description="category name. john / su / alex")
