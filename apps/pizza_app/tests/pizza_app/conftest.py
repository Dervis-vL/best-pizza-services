"""Shared test fixtures for pizza_app tests."""

from unittest.mock import MagicMock

import pandas as pd
import pytest

from pizza_app import repositories, schemas
from pizza_app.infrastructure import PizzaDataAdapter


@pytest.fixture
def sample_locations_df() -> pd.DataFrame:
    """Valid pizzeria DataFrame matching PizzeriaSchema."""
    data = {
        "slug": ["da-michele", "sorbillo"],
        "latitude": [40.8518, 40.8530],
        "longitude": [14.2681, 14.2560],
        "country": ["Italy", "Italy"],
        "city": ["Naples", "Naples"],
    }
    return schemas.PizzeriaSchema.validate(pd.DataFrame(data))


@pytest.fixture
def sample_rankings_df() -> pd.DataFrame:
    """Valid rankings DataFrame matching RankingSchema."""
    data = {
        "pizzeria_name": ["da-michele", "sorbillo"],
        "position": [1.0, 2.0],
        "year": [2024, 2024],
        "category": ["50 Top Pizza Italia", "50 Top Pizza Italia"],
    }
    return schemas.RankingSchema.validate(pd.DataFrame(data))


@pytest.fixture
def mock_repo(
    sample_locations_df: pd.DataFrame,
    sample_rankings_df: pd.DataFrame,
) -> MagicMock:
    """Mock PizzaPlatformDatabase returning valid sample data."""
    repo = MagicMock(spec=repositories.PizzaPlatformDatabase)
    repo.read_pizzerias.return_value = sample_locations_df
    repo.read_rankings.return_value = sample_rankings_df
    return repo


@pytest.fixture
def adapter(mock_repo: MagicMock):
    """PizzaDataAdapter with mock repo and a clean cache for each test."""
    PizzaDataAdapter.load_pizza_data.clear()
    yield PizzaDataAdapter(repo=mock_repo)
    PizzaDataAdapter.load_pizza_data.clear()
