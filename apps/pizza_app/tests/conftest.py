"""Tests root level fixtures for the pizza app."""

from collections.abc import Generator

import pytest
from tenacity import wait_none

from pizza_app import repositories


@pytest.fixture(name="no_retry_sleep_fixture", autouse=True)
def no_retry_sleep() -> Generator[None]:
    """Strip the backoff so retry tests don't actually sleep."""
    original = repositories.PizzaPlatformAPI.read_pizzerias.retry.wait  # pylint: disable=no-member
    repositories.PizzaPlatformAPI.read_pizzerias.retry.wait = wait_none()  # pylint: disable=no-member
    yield
    repositories.PizzaPlatformAPI.read_pizzerias.retry.wait = original  # pylint: disable=no-member
