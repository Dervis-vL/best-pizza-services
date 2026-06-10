"""Tests for the PizzaDataAdapter."""

from unittest.mock import MagicMock

import pandas as pd

from pizza_app import dataclasses as pizza_dataclasses
from pizza_app import schemas
from pizza_app.infrastructure import PizzaDataAdapter


def test_load_pizza_data_returns_pizza_data(adapter_fixture: PizzaDataAdapter) -> None:
    """Test that load_pizza_data returns a populated PizzaData dataclass."""
    # GIVEN an adapter backed by a repo with valid data

    # WHEN load_pizza_data is called
    result = adapter_fixture.load_pizza_data()

    # THEN a PizzaData instance is returned with non-empty DataFrames
    assert isinstance(result, pizza_dataclasses.PizzaData)
    assert not result.locations.empty
    assert not result.rankings.empty
    assert not result.awards.empty


def test_load_pizza_data_caches_result(
    adapter_fixture: PizzaDataAdapter,
    mock_repo_fixture: MagicMock,
) -> None:
    """Test that repeated calls return cached data without calling the API again."""
    # GIVEN an adapter with a fresh cache

    # WHEN load_pizza_data is called twice
    result_1 = adapter_fixture.load_pizza_data()
    result_2 = adapter_fixture.load_pizza_data()

    # THEN the API is only called once — the second call hits the cache
    mock_repo_fixture.read_pizzerias.assert_called_once()
    pd.testing.assert_frame_equal(result_1.locations, result_2.locations)
    pd.testing.assert_frame_equal(result_1.rankings, result_2.rankings)
    pd.testing.assert_frame_equal(result_1.awards, result_2.awards)


def test_load_pizza_data_locations_match_schema(adapter_fixture: PizzaDataAdapter) -> None:
    """Test that the locations DataFrame conforms to LocationSchema."""
    # GIVEN an adapter backed by valid data

    # WHEN load_pizza_data is called
    result = adapter_fixture.load_pizza_data()

    # THEN the locations DataFrame passes schema validation
    schemas.LocationSchema.validate(result.locations)


def test_load_pizza_data_rankings_match_schema(adapter_fixture: PizzaDataAdapter) -> None:
    """Test that the rankings DataFrame conforms to RankingSchema."""
    # GIVEN an adapter backed by valid data

    # WHEN load_pizza_data is called
    result = adapter_fixture.load_pizza_data()

    # THEN the rankings DataFrame passes schema validation
    schemas.RankingSchema.validate(result.rankings)


def test_load_pizza_data_awards_match_schema(adapter_fixture: PizzaDataAdapter) -> None:
    """Test that the awards DataFrame conforms to AwardSchema."""
    # GIVEN an adapter backed by valid data

    # WHEN load_pizza_data is called
    result = adapter_fixture.load_pizza_data()

    # THEN the awards DataFrame passes schema validation
    schemas.AwardSchema.validate(result.awards)


def test_load_pizza_data_frames_share_join_key(adapter_fixture: PizzaDataAdapter) -> None:
    """Test that rankings and awards reference slugs present in locations."""
    # GIVEN an adapter backed by valid data

    # WHEN load_pizza_data is called
    result = adapter_fixture.load_pizza_data()

    # THEN every ranking and award row joins to a location via the slug
    slugs = set(result.locations[schemas.LocationSchema.slug])
    assert set(result.rankings[schemas.RankingSchema.pizzeria_name]) <= slugs
    assert set(result.awards[schemas.AwardSchema.pizzeria_name]) <= slugs
