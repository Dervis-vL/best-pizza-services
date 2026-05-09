"""Schema for ranking data."""

import pandera.pandas as pa
from pandera import typing as pa_typing

from pizza_platform_shared import enums


class RankingSchema(pa.DataFrameModel):
    """Validates a flat DataFrame of all pizzeria ranking entries.

    Columns:
        pizzeria_name: Display name of the pizzeria.
        position:      Rank position (nullable — some entries only have an award).
        year:          Edition year.
        category:      Category name (e.g. 'Top 50 World').
    """

    pizzeria_name: pa_typing.Series[str] = pa.Field(
        nullable=False, str_length={"min_value": 1}
    )
    position: pa_typing.Series[float] = pa.Field(nullable=True, ge=1)
    year: pa_typing.Series[int] = pa.Field(
        nullable=False, isin=[y.value for y in enums.Year]
    )
    category: pa_typing.Series[str] = pa.Field(
        nullable=False, str_length={"min_value": 1}, isin=enums.BaseCategories.list()
    )

    class Config:  # pylint: disable=too-few-public-methods
        """Config."""

        strict = True
        coerce = True
        name = "RankingSchema"
