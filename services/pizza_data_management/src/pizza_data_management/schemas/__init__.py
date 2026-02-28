"""Schemas for the pizza data scraper."""

from pizza_data_management.schemas.category import CategorySchema
from pizza_data_management.schemas.locations import LocationSchema
from pizza_data_management.schemas.pizzeria import PizzeriaSchema
from pizza_data_management.schemas.ranked_edition import RankedEditionSchema
from pizza_data_management.schemas.ranking_position import RankingPositionSchema
from pizza_data_management.schemas.endpoints import (
    RankingEndpointsSchema,
    PizzeriaEndpointsSchema
)
from pizza_data_management.schemas.webpages import WebpagesSchema

__all__ = [
    "CategorySchema",
    "LocationSchema",
    "PizzeriaSchema",
    "RankedEditionSchema",
    "RankingEndpointsSchema",
    "RankingPositionSchema",
    "PizzeriaEndpointsSchema",
    "WebpagesSchema",
]