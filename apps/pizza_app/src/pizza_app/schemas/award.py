"""Award pandera schema."""

import pandas as pd
import pandera.pandas as pa
from pandera import typing as pa_typing

from pizza_app import enums
from pizza_platform_shared import enums as shared_enums
from pizza_platform_shared import schemas as shared_schemas


class AwardSchema(pa.DataFrameModel):
    """Validates a flat DataFrame of all pizzeria award entries.

    Columns:
        pizzeria_name: Slug of the pizzeria (join key with LocationSchema.slug).
        award:         Name of the award.
        sponsor:       Sponsor of the award.
        year:          Edition year.
        category:      Category name (e.g. 'Top Pizza Italia').
    """

    pizzeria_name: pa_typing.Series[str] = pa.Field(
        nullable=False,
        str_length={"min_value": 1},
    )
    award: pa_typing.Series[str] = pa.Field(
        nullable=False,
        str_length={"min_value": 1},
    )
    sponsor: pa_typing.Series[str] = pa.Field(nullable=False)
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
    ) -> pa_typing.DataFrame[AwardSchema]:
        """Create an AwardSchema DataFrame by flattening the awards from PizzeriaReadSchema."""
        records = [
            {
                cls.pizzeria_name: pizzeria.name,
                cls.award: award.award,
                cls.sponsor: award.sponsor,
                cls.year: award.edition.year,
                cls.category: award.edition.category.name,
            }
            for pizzeria in pizzerias
            for award in pizzeria.awards
        ]
        columns = [
            cls.pizzeria_name,
            cls.award,
            cls.sponsor,
            cls.year,
            cls.category,
        ]
        return cls.validate(pd.DataFrame(records, columns=columns))

    class Config:  # pylint: disable=too-few-public-methods
        """Config."""

        strict = True
        coerce = True
        name = "AwardSchema"
