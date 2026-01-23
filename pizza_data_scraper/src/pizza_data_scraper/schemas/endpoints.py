"""Endpoints schemas for pizza data scraper."""

import pandera.pandas as pa
from pandera import typing as pa_typing


class Endpoints(pa.DataFrameModel):
    """Schema for the endpoints."""

    class Config:  # pylint: disable=too-few-public-methods
        """Configure schema to coerce types, and filter extra fields.

        Set coerce equal to true to enforce correct data types.
        """

        coerce = True
        strict = "filter"

    year: pa_typing.Series[str] = pa.Field(description="Year of the ranked data endpoint")
    category: pa_typing.Series[str] = pa.Field(description="Category of the ranked data endpoint")
    endpoint: pa_typing.Series[str] = pa.Field(description="Endpoint URL to the ranked data")