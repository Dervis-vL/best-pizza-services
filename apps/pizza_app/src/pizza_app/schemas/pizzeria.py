"""Pizzeria pandera schema."""

import pandera.pandas as pa
from pandera import typing as pa_typing


class PizzeriaSchema(pa.DataFrameModel):
    """Validates a DataFrame of pizzerias that have known coordinates.

    Columns:
        name: Display name of the pizzeria.
        lat:  Latitude, must be within valid geographic range.
        lng:  Longitude, must be within valid geographic range.
    """

    name: pa_typing.Series[str] = pa.Field(nullable=False, str_length={"min_value": 1})
    latitude: pa_typing.Series[float] = pa.Field(nullable=False, ge=-90, le=90)
    longitude: pa_typing.Series[float] = pa.Field(nullable=False, ge=-180, le=180)

    class Config:
        """Config."""
        strict = True
        coerce = True
        name = "PizzeriaSchema"
