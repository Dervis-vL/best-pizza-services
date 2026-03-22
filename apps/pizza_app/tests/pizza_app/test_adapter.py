"""Tests for the PizzaDataAdapter."""

import pandas as pd
from unittest.mock import MagicMock

from pizza_app import dataclasses as pizza_dataclasses, schemas
from pizza_app.infrastructure import PizzaDataAdapter


def test_load_pizza_data_returns_pizza_data(adapter: PizzaDataAdapter) -> None:
    """Test that load_pizza_data returns a populated PizzaData dataclass."""
    # GIVEN an adapter backed by a repo with valid data

    # WHEN load_pizza_data is called
    result = adapter.load_pizza_data()

    # THEN a PizzaData instance is returned with non-empty DataFrames
    assert isinstance(result, pizza_dataclasses.PizzaData)
    assert not result.locations.empty
    assert not result.rankings.empty


def test_load_pizza_data_caches_result(
    adapter: PizzaDataAdapter,
    mock_repo: MagicMock,
) -> None:
    """Test that repeated calls return cached data without querying the DB again."""
    # GIVEN an adapter with a fresh cache

    # WHEN load_pizza_data is called twice
    result_1 = adapter.load_pizza_data()
    result_2 = adapter.load_pizza_data()

    # THEN the repo is only queried once — the second call hits the cache
    mock_repo.read_pizzerias.assert_called_once()
    mock_repo.read_rankings.assert_called_once()
    pd.testing.assert_frame_equal(result_1.locations, result_2.locations)
    pd.testing.assert_frame_equal(result_1.rankings, result_2.rankings)


def test_load_pizza_data_locations_match_schema(adapter: PizzaDataAdapter) -> None:
    """Test that the locations DataFrame conforms to PizzeriaSchema."""
    # GIVEN an adapter backed by valid data

    # WHEN load_pizza_data is called
    result = adapter.load_pizza_data()

    # THEN the locations DataFrame passes schema validation
    schemas.PizzeriaSchema.validate(result.locations)


def test_load_pizza_data_rankings_match_schema(adapter: PizzaDataAdapter) -> None:
    """Test that the rankings DataFrame conforms to RankingSchema."""
    # GIVEN an adapter backed by valid data

    # WHEN load_pizza_data is called
    result = adapter.load_pizza_data()

    # THEN the rankings DataFrame passes schema validation
    schemas.RankingSchema.validate(result.rankings)
