"""Pizzeria pandera schema."""

import pandera as pa
from pandera import typing as pa_typing


class PizzeriaSchema(pa.DataFrameModel):
    """Validates a DataFrame of pizzerias that have known coordinates.

    Columns:
        name: Display name of the pizzeria.
        lat:  Latitude, must be within valid geographic range.
        lng:  Longitude, must be within valid geographic range.
    """

    name: pa_typing.Series[str] = pa.Field(nullable=False, str_length={"min_value": 1})
    latitude: pa_typing.Series[float] = pa.Field(nullable=False)
    longitude: pa_typing.Series[float] = pa.Field(nullable=False)

    class Config:
        strict = True
        coerce = True
        name = "PizzeriaSchema"