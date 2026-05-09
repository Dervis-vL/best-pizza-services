"""Abstract base class for object storage repositories."""

from __future__ import annotations

import logging

import boto3

from pizza_data_storage import constants, enums, settings

logger = logging.getLogger(__name__)


class BaseStorage:  # pylint: disable=too-few-public-methods
    """Base class for S3-compatible object storage repositories."""

    def __init__(self, client: boto3.client, bucket: str) -> None:
        """Initialize the storage repository."""
        self._client = client
        self._bucket = bucket

    @classmethod
    def from_settings(
        cls, storage_settings: settings.PizzaStorageSettings
    ) -> "BaseStorage":
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
        return f"{constants.StorageKeys.SCRAPES_PREFIX}/{model_name.value}/id_{model_id}.html"

    @staticmethod
    def _build_prefix(
        *,
        model_name: enums.HtmlModelName | None = None,
    ) -> str:
        """Build an S3 prefix for listing, as specific as the filters allow."""
        if model_name:
            return f"{constants.StorageKeys.SCRAPES_PREFIX}/{model_name.value}/"
        return f"{constants.StorageKeys.SCRAPES_PREFIX}/"
