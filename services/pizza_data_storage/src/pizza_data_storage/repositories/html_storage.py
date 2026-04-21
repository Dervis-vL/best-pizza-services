"""HTML file storage repository using S3-compatible object storage."""

from __future__ import annotations

import logging

from botocore.exceptions import ClientError

from pizza_platform_shared import repositories as shared_repos

logger = logging.getLogger(__name__)

_SCRAPES_PREFIX = "scrapes"
_GLACIER = "GLACIER"


class HtmlStorageRepository(shared_repos.BaseStorage):
    """Repository for storing and retrieving scraped HTML files."""

    def save_edition_html(
        self,
        *,
        html: str,
        category_id: str,
        year: int,
    ) -> str:
        """Store an edition's HTML string in Glacier object storage."""
        key = self._build_key(category_id=category_id, year=year)

        self._client.put_object(
            Bucket=self._bucket,
            Key=key,
            Body=html.encode("utf-8"),
            ContentType="text/html; charset=utf-8",
            StorageClass=_GLACIER,
        )
        logger.info("Stored edition HTML at key=%s", key)
        return key

    def get_edition_html(self, *, key: str) -> str:
        """Retrieve an edition's HTML string from object storage."""
        try:
            response = self._client.get_object(Bucket=self._bucket, Key=key)
            html = response["Body"].read().decode("utf-8")
            logger.info("Retrieved edition HTML from key=%s", key)
            return html
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                raise KeyError(f"No HTML found at key: {key}") from e
            raise

    def list_edition_keys(
        self,
        *,
        category_id: str | None = None,
        year: int | None = None,
    ) -> list[str]:
        """List stored edition HTML keys, optionally filtered by category or year."""
        prefix = self._build_prefix(category_id=category_id, year=year)
        response = self._client.list_objects_v2(
            Bucket=self._bucket,
            Prefix=prefix,
        )
        keys = [obj["Key"] for obj in response.get("Contents", [])]
        logger.info("Listed %d keys under prefix=%s", len(keys), prefix)
        return keys

    def edition_html_exists(self, *, category_id: str, year: int) -> bool:
        """Check whether an edition HTML file already exists in storage."""
        key = self._build_key(category_id=category_id, year=year)
        try:
            self._client.head_object(Bucket=self._bucket, Key=key)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            raise

    @staticmethod
    def _build_key(*, category_id: str, year: int) -> str:
        """Build the canonical object key for an edition HTML file."""
        return f"{_SCRAPES_PREFIX}/{category_id}/{year}/{category_id}_{year}.html"

    @staticmethod
    def _build_prefix(
        *,
        category_id: str | None,
        year: int | None,
    ) -> str:
        """Build an S3 prefix for listing, as specific as the filters allow."""
        if category_id and year:
            return f"{_SCRAPES_PREFIX}/{category_id}/{year}/"
        if category_id:
            return f"{_SCRAPES_PREFIX}/{category_id}/"
        return f"{_SCRAPES_PREFIX}/"
