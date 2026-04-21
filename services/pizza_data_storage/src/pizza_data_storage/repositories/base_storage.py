"""Abstract base class for object storage repositories."""

from __future__ import annotations

import logging

import boto3

from pizza_data_storage import settings

logger = logging.getLogger(__name__)


class BaseStorage:
    """Base class for S3-compatible object storage repositories."""

    def __init__(self, client: boto3.client, bucket: str) -> None:
        """Initialize the storage repository."""
        self._client = client
        self._bucket = bucket

    @classmethod
    def from_settings(cls, storage_settings: settings.PizzaStorageSettings) -> "BaseStorage":
        """Create a storage repo instance from settings."""
        client = boto3.client(
            "s3",
            endpoint_url=str(storage_settings.endpoint),
            aws_access_key_id=storage_settings.key_id,
            aws_secret_access_key=storage_settings.secret.get_secret_value(),
            region_name=storage_settings.region
        )
        return cls(client=client, bucket=storage_settings.bucket)
