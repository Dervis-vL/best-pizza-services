"""Pizza platform pydantic schemas."""

from pizza_platform_shared.schemas.award import AwardReadSchema, AwardSchema
from pizza_platform_shared.schemas.category import CategoryReadSchema, CategorySchema
from pizza_platform_shared.schemas.edition import EditionReadSchema, EditionSchema
from pizza_platform_shared.schemas.location import LocationReadSchema, LocationSchema
from pizza_platform_shared.schemas.pizzeria import PizzeriaReadSchema, PizzeriaSchema
from pizza_platform_shared.schemas.ranking import RankingReadSchema, RankingSchema
from pizza_platform_shared.schemas.webpage import WebpageReadSchema, WebpageSchema

__all__ = [
    "AwardReadSchema",
    "AwardSchema",
    "CategoryReadSchema",
    "CategorySchema",
    "EditionReadSchema",
    "EditionSchema",
    "LocationReadSchema",
    "LocationSchema",
    "PizzeriaReadSchema",
    "PizzeriaSchema",
    "RankingReadSchema",
    "RankingSchema",
    "WebpageReadSchema",
    "WebpageSchema",
]
