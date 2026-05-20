"""Abstract base class for object storage repositories."""

import logging
from typing import TYPE_CHECKING, Self

import boto3

from pizza_platform_shared import constants, enums
from pizza_platform_shared.settings.pizza_storage import PizzaStorageSettings

if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client

logger = logging.getLogger(__name__)


class BaseStorage:  # pylint: disable=too-few-public-methods
    """Base class for S3-compatible object storage repositories."""

    def __init__(self, client: S3Client, bucket: str) -> None:
        """Initialize the storage repository."""
        self._client = client
        self._bucket = bucket

    @classmethod
    def from_settings(
        cls,
        storage_settings: PizzaStorageSettings,
    ) -> Self:
        """Create a storage repo instance from settings."""
        client = boto3.client(
            constants.StorageKeys.STORAGE_TYPE,
            endpoint_url=str(storage_settings.endpoint),
            aws_access_key_id=storage_settings.key_id,
            aws_secret_access_key=storage_settings.secret.get_secret_value(),
            region_name=storage_settings.region,
        )
        return cls(client=client, bucket=storage_settings.bucket)

    @staticmethod
    def _build_key(*, model_name: enums.HtmlModelName, model_id: int) -> str:
        """Build the canonical object key for an edition HTML file."""
        prefix = constants.StorageKeys.SCRAPES_PREFIX
        return f"{prefix}/{model_name.value}/id_{model_id}.html"

    @staticmethod
    def _build_prefix(
        *,
        model_name: enums.HtmlModelName | None = None,
    ) -> str:
        """Build an S3 prefix for listing, as specific as the filters allow."""
        if model_name:
            return f"{constants.StorageKeys.SCRAPES_PREFIX}/{model_name.value}/"
        return f"{constants.StorageKeys.SCRAPES_PREFIX}/"
