"""Schema for ranking data."""

import pandas as pd
import pandera.pandas as pa
from pandera import typing as pa_typing

from pizza_app import enums
from pizza_platform_shared import enums as shared_enums
from pizza_platform_shared import schemas as shared_schemas


class RankingSchema(pa.DataFrameModel):
    """Validates a flat DataFrame of all pizzeria ranking entries.

    Columns:
        pizzeria_name: Display name of the pizzeria.
        position:      Rank position (nullable — some entries only have an award).
        year:          Edition year.
        category:      Category name (e.g. 'Top 50 World').
    """

    pizzeria_name: pa_typing.Series[str] = pa.Field(
        nullable=False,
        str_length={"min_value": 1},
    )
    position: pa_typing.Series[float] = pa.Field(nullable=True, ge=1)
    year: pa_typing.Series[int] = pa.Field(
        nullable=False,
        isin=[y.value for y in shared_enums.Year],
    )
    category: pa_typing.Series[str] = pa.Field(
        nullable=False,
        str_length={"min_value": 1},
        isin=enums.BaseCategories.list(),
    )

    @classmethod
    def from_pizzeria_schema(
        cls, pizzerias: list[shared_schemas.PizzeriaReadSchema]
    ) -> pa_typing.DataFrame[RankingSchema]:
        """Create a RankingSchema DataFrame by flattening the rankings from PizzeriaReadSchema."""
        records = [
            {
                cls.pizzeria_name: pizzeria.name,
                cls.position: ranking.position,
                cls.year: ranking.edition.year,
                cls.category: ranking.edition.category.name,
            }
            for pizzeria in pizzerias
            for ranking in pizzeria.rankings
        ]
        columns = [
            cls.pizzeria_name,
            cls.position,
            cls.year,
            cls.category,
        ]
        return cls.validate(pd.DataFrame(records, columns=columns))

    class Config:  # pylint: disable=too-few-public-methods
        """Config."""

        strict = True
        coerce = True
        name = "RankingSchema"
