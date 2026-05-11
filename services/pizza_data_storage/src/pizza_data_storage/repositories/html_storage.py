"""HTML file storage repository using S3-compatible object storage."""

from __future__ import annotations

import logging

from botocore.exceptions import ClientError

from pizza_data_storage import constants, enums
from pizza_platform_shared import repositories as shared_repos

logger = logging.getLogger(__name__)


class HtmlStorageRepository(shared_repos.BaseStorage):
    """Repository for storing and retrieving scraped HTML files."""

    def save_html(
        self,
        *,
        html: str,
        model_id: int,
        model_name: enums.HtmlModelName,
    ) -> str:
        """Store an HTML string in Glacier object storage."""
        key = self._build_key(
            model_name=model_name,
            model_id=model_id,
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

    def get_html(self, *, model_name: enums.HtmlModelName, model_id: int) -> str:
        """Retrieve an edition's HTML string from object storage."""
        key = self._build_key(
            model_name=model_name,
            model_id=model_id,
        )

        try:
            response = self._client.get_object(Bucket=self._bucket, Key=key)
            html = response["Body"].read().decode("utf-8")
            logger.info("Retrieved %s HTML from key=%s", model_name, key)
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                msg = f"No HTML found at key: {key}"
                raise KeyError(msg) from e
            raise
        return html

    def list_keys(self, *, model_name: enums.HtmlModelName | None = None) -> list[str]:
        """List stored edition HTML keys, optionally filtered by category or year."""
        prefix = self._build_prefix(model_name=model_name)
        response = self._client.list_objects_v2(
            Bucket=self._bucket,
            Prefix=prefix,
        )
        keys = [obj["Key"] for obj in response.get("Contents", [])]
        logger.info("Listed %d keys under prefix=%s", len(keys), prefix)
        return keys

    def html_exists(self, *, model_id: int, model_name: enums.HtmlModelName) -> bool:
        """Check whether an edition HTML file already exists in storage."""
        key = self._build_key(model_name=model_name, model_id=model_id)

        try:
            self._client.head_object(Bucket=self._bucket, Key=key)
            logger.info(
                "HTML exists for %s with id=%s at key=%s",
                model_name,
                model_id,
                key,
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            raise
        return True
