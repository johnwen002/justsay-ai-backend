import os
from functools import lru_cache
from typing import Optional

from pydantic import PostgresDsn, RedisDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigBase(BaseSettings):
    GEMINI_API_KEY: str = "AIzaSyD0VoslJi9534QVk8Dvkmm0dl4tm8K3lLw"

    # TOKEN
    SECRET_KEY: str = "a035e292-1b1f-4105-b477-302769c78a1f"
    ACCESS_TOKEN_EXPIRES: int = 30
    ALGORITHM: str = "HS256"
    REFRESH_TOKEN_EXPIRES: int = 60 * 60 * 24 * 30

    # QDRANT
    QDRANT_URL: str
    QDRANT_API_KEY: str
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # MINIO
    MINIO_SERVER: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET_NAME: str
    MINIO_CHUNK_SIZE: int = 5 * 1024 * 1024

    # POSTGRES
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    ASYNC_SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    SYNC_SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    SQLALCHEMY_POOL_SIZE: int = 50
    SQLALCHEMY_POOL_PRE_PING: bool = False
    SQLALCHEMY_POOL_RECYCLE: int = 300
    SQLALCHEMY_ECHO: bool = False

    @field_validator("ASYNC_SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_async_db_connection(cls, v: Optional[str], values: ValidationInfo):
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_SERVER"),
            path=f"{values.data.get('POSTGRES_DB') or ''}",
        )

    @field_validator("SYNC_SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_sync_db_connection(cls, v: Optional[str], values: ValidationInfo):
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_SERVER"),
            path=f"{values.data.get('POSTGRES_DB') or ''}",
        )

    # REDIS
    REDIS_SERVER: str
    REDIS_PASSWORD: str
    REDIS_DB: int = 0
    REDIS_URI: Optional[RedisDsn] = None

    @field_validator("REDIS_URI", mode="before")
    def assemble_redis_connection(
        cls, v: Optional[str], values: ValidationInfo
    ):  # noqa
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme="redis",
            password=values.data.get("REDIS_PASSWORD"),
            host=values.data.get("REDIS_SERVER"),
            path=f"{values.data.get('REDIS_DB') or ''}",
        )


class ConfigDev(ConfigBase):
    model_config = SettingsConfigDict(env_file=".env.dev")


class ConfigProd(ConfigBase):
    model_config = SettingsConfigDict(env_file=".env.prod")


@lru_cache
def get_settings():
    return ConfigDev() if os.getenv("ENV") == "DEV" else ConfigProd()


settings = get_settings()


FIRECRAWL_KEYS = [
    "fc-26b4e86458ba465f9b1c669db643c1d2",
    "fc-01cbb42175f7429fb619b251819d82d8",
    "fc-5d9cc1c87c624e87a8e61dadbee22228",
]
