"""HTML file storage repository using S3-compatible object storage."""

from __future__ import annotations

import logging
from typing import Literal

from botocore.exceptions import ClientError

from pizza_platform_shared import repositories as shared_repos
from pizza_data_storage import constants

logger = logging.getLogger(__name__)


class HtmlStorageRepository(shared_repos.BaseStorage):
    """Repository for storing and retrieving scraped HTML files."""

    def save_html(
        self,
        *,
        html: str,
        model_id: str,
        model_name: Literal["editions", "webpages"],
    ) -> str:
        """Store an HTML string in Glacier object storage."""
        key = self._build_key(
            model_name=model_id,
            model_id=model_name,
        )

        self._client.put_object(
            Bucket=self._bucket,
            Key=key,
            Body=html.encode("utf-8"),
            ContentType="text/html; charset=utf-8",
            StorageClass=constants.StorageKeys.STORAGE_TIER,
        )
        logger.info("Stored %s HTML at key=%s", model_name, key)
        return key

    def get_html(self, *, model_name: Literal["editions", "webpages"], model_id: str) -> str:
        """Retrieve an edition's HTML string from object storage."""
        key = self._build_key(
            model_name=model_name,
            model_id=model_id,
        )

        try:
            response = self._client.get_object(Bucket=self._bucket, Key=key)
            html = response["Body"].read().decode("utf-8")
            logger.info("Retrieved %s HTML from key=%s", model_name, key)
            return html
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                raise KeyError(f"No HTML found at key: {key}") from e
            raise

    def list_keys(self, *, model_name: Literal["editions", "webpages"] | None = None) -> list[str]:
        """List stored edition HTML keys, optionally filtered by category or year."""
        prefix = self._build_prefix(model_name=model_name)
        response = self._client.list_objects_v2(
            Bucket=self._bucket,
            Prefix=prefix,
        )
        keys = [obj["Key"] for obj in response.get("Contents", [])]
        logger.info("Listed %d keys under prefix=%s", len(keys), prefix)
        return keys

    def html_exists(self, *, model_id: str, model_name: Literal["editions", "webpages"]) -> bool:
        """Check whether an edition HTML file already exists in storage."""
        key = self._build_key(model_name=model_name, model_id=model_id)

        try:
            self._client.head_object(Bucket=self._bucket, Key=key)
            logger.info("HTML exists for %s with id=%s at key=%s", model_name, model_id, key)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            raise

    @staticmethod
    def _build_key(*, model_name: str, model_id: str) -> str:
        """Build the canonical object key for an edition HTML file."""
        return f"{constants.StorageKeys.SCRAPES_PREFIX}/{model_name}/id_{model_id}.html"

    @staticmethod
    def _build_prefix(
        *,
        model_name: Literal["editions", "webpages"] | None = None,
    ) -> str:
        """Build an S3 prefix for listing, as specific as the filters allow."""
        if model_name:
            return f"{constants.StorageKeys.SCRAPES_PREFIX}/{model_name}/"
        return f"{constants.StorageKeys.SCRAPES_PREFIX}/"
