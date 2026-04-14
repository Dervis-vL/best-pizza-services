"""Pizza platform pydantic schemas."""

from pizza_platform_shared.schemas.category import CategoryReadSchema, CategorySchema
from pizza_platform_shared.schemas.edition import EditionReadSchema, EditionSchema
from pizza_platform_shared.schemas.locations import LocationReadSchema, LocationSchema
from pizza_platform_shared.schemas.pizzeria import PizzeriaReadSchema, PizzeriaSchema
from pizza_platform_shared.schemas.ranking import RankingReadSchema, RankingSchema
from pizza_platform_shared.schemas.webpages import WebpagesReadSchema, WebpagesSchema

__all__ = [
    "CategorySchema",
    "CategoryReadSchema",
    "LocationSchema",
    "LocationReadSchema",
    "EditionSchema",
    "EditionReadSchema",
    "RankingSchema",
    "RankingReadSchema",
    "PizzeriaSchema",
    "PizzeriaReadSchema",
    "WebpagesSchema",
    "WebpagesReadSchema",
]
