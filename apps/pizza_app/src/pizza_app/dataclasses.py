"""Pizza app dataclasses."""

from dataclasses import dataclass

from pandera import typing as pa_typing

from pizza_app import schemas


@dataclass
class PizzaData:
    """Pizza dataclass."""

    locations: pa_typing.DataFrame[schemas.PizzeriaSchema]
    rankings: pa_typing.DataFrame[schemas.RankingSchema]
