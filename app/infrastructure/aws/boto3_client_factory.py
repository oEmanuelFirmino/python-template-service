from functools import lru_cache

from boto3 import client as boto3_client
from botocore.config import Config
from app.core.settings import settings


class AWSClientFactory:

    @staticmethod
    @lru_cache
    def create(service_name: str, config: Config | None = None):
        return boto3_client(
            service_name=service_name,
            region_name=settings.aws_region,
            config=config,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )
