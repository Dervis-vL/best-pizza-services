"""Pizzeria pandera schema."""

import pandas as pd
import pandera.pandas as pa
from pandera import typing as pa_typing

from pizza_platform_shared import schemas as shared_schemas

_UNKNOWN = "Unknown"


class LocationSchema(pa.DataFrameModel):
    """Validates a DataFrame of pizzerias location that have known coordinates.

    Columns:
        name: Display name of the pizzeria.
        lat:  Latitude, must be within valid geographic range.
        lng:  Longitude, must be within valid geographic range.
        country: Country name (nullable).
        city: City name (nullable).
    """

    name: pa_typing.Series[str] = pa.Field(nullable=False, str_length={"min_value": 1})
    slug: pa_typing.Series[str] = pa.Field(nullable=False, str_length={"min_value": 1})
    latitude: pa_typing.Series[float] = pa.Field(nullable=False, ge=-90, le=90)
    longitude: pa_typing.Series[float] = pa.Field(nullable=False, ge=-180, le=180)
    country: pa_typing.Series[str] = pa.Field(
        nullable=False,
        str_length={"min_value": 1},
    )
    city: pa_typing.Series[str] = pa.Field(nullable=False)

    @pa.dataframe_parser
    @classmethod
    def derive_name(
        cls, df: pa_typing.DataFrame[LocationSchema]
    ) -> pa_typing.DataFrame[LocationSchema]:
        """Derive name from slug"""
        df = df.copy()
        df["name"] = df["slug"].apply(
            lambda val: " ".join(word.capitalize() for word in val.split("-")),
        )
        return df

    @classmethod
    def from_pizzeria_schema(
        cls, pizzerias: list[shared_schemas.PizzeriaReadSchema]
    ) -> pa_typing.DataFrame[LocationSchema]:
        """Create a LocationSchema DataFrame by flattening the locations from PizzeriaReadSchema."""
        records = [
            {
                cls.slug: pizzeria.name,
                cls.latitude: location.latitude,
                cls.longitude: location.longitude,
                cls.country: location.country or _UNKNOWN,
                cls.city: location.city or _UNKNOWN,
            }
            for pizzeria in pizzerias
            for location in pizzeria.locations
            if location.has_coordinates
        ]
        columns = [
            cls.slug,
            cls.latitude,
            cls.longitude,
            cls.country,
            cls.city,
        ]
        return cls.validate(pa_typing.cast(pd.DataFrame, records)[columns])

    class Config:
        """Config."""

        strict = True
        coerce = True
        name = "PizzeriaSchema"
