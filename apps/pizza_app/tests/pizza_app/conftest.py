"""Shared test fixtures for pizza_app tests."""

from collections.abc import Generator
from unittest.mock import MagicMock

import pytest

from pizza_app import repositories
from pizza_app.infrastructure import PizzaDataAdapter
from pizza_platform_shared import schemas as shared_schemas


@pytest.fixture(name="sample_pizzerias_fixture")
def sample_pizzerias() -> list[shared_schemas.PizzeriaReadSchema]:
    """Pizzeria read models as returned by the API, with nested relationships."""
    edition = shared_schemas.EditionReadSchema(
        id=1,
        year=2024,
        url="https://example.com/rankings/2024",
        category_id=1,
        category=shared_schemas.CategoryReadSchema(
            id=1,
            slug="50-top-pizza-italia",
            name="50 Top Pizza Italia",
            description="Best pizzerias in Italy.",
        ),
    )
    return [
        shared_schemas.PizzeriaReadSchema(
            id=1,
            name="Da Michele",
            locations=[
                shared_schemas.LocationReadSchema(
                    id=1,
                    pizzeria_id=1,
                    city="Naples",
                    country="Italy",
                    latitude=40.8518,
                    longitude=14.2681,
                ),
            ],
            rankings=[
                shared_schemas.RankingReadSchema(
                    id=1,
                    position=1,
                    edition_id=1,
                    pizzeria_id=1,
                    edition=edition,
                ),
            ],
            awards=[
                shared_schemas.AwardReadSchema(
                    id=1,
                    award="Pizza of the Year",
                    sponsor="Latteria Sorrentina",
                    edition_id=1,
                    pizzeria_id=1,
                    edition=edition,
                ),
            ],
        ),
        shared_schemas.PizzeriaReadSchema(
            id=2,
            name="Sorbillo",
            locations=[
                shared_schemas.LocationReadSchema(
                    id=2,
                    pizzeria_id=2,
                    city="Naples",
                    country="Italy",
                    latitude=40.8530,
                    longitude=14.2560,
                ),
            ],
            rankings=[
                shared_schemas.RankingReadSchema(
                    id=2,
                    position=2,
                    edition_id=1,
                    pizzeria_id=2,
                    edition=edition,
                ),
            ],
        ),
    ]


@pytest.fixture(name="mock_repo_fixture")
def mock_repo(
    sample_pizzerias_fixture: list[shared_schemas.PizzeriaReadSchema],
) -> MagicMock:
    """Mock PizzaPlatformAPI returning valid pizzeria read models."""
    repo = MagicMock(spec=repositories.PizzaPlatformAPI)
    repo.read_pizzerias.return_value = sample_pizzerias_fixture
    return repo


@pytest.fixture(name="adapter_fixture")
def adapter(mock_repo_fixture: MagicMock) -> Generator[PizzaDataAdapter]:
    """PizzaDataAdapter with mock repo and a clean cache for each test."""
    PizzaDataAdapter.load_data.clear()  # pylint: disable=no-member
    yield PizzaDataAdapter(repo=mock_repo_fixture)
    PizzaDataAdapter.load_data.clear()  # pylint: disable=no-member
