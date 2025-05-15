from functools import lru_cache
from fastapi import HTTPException
from loguru import logger
from minio import Minio, S3Error

from src.config import settings


@lru_cache
def get_minio_client() -> Minio:
    # 初始化 MinIO 客户端
    minio_client = Minio(
        settings.MINIO_SERVER,  # MinIO 服务器地址
        access_key=settings.MINIO_ACCESS_KEY,  # 访问密钥
        secret_key=settings.MINIO_SECRET_KEY,  # 密码
        secure=False,  # 是否使用 HTTPS
    )
    # 确保 bucket 存在
    try:
        if not minio_client.bucket_exists(settings.MINIO_BUCKET_NAME):
            minio_client.make_bucket(settings.MINIO_BUCKET_NAME)
    except S3Error as e:
        logger.error(f"MinIO 错误: {e}")
        raise HTTPException(status_code=500, detail="存储服务配置错误")
    return minio_client
