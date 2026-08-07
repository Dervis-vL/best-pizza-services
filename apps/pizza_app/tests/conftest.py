"""Tests root level fixtures for the pizza app."""

from collections.abc import Generator
from pathlib import Path

import pytest
from dotenv import load_dotenv
from tenacity import wait_none

from pizza_app import repositories

load_dotenv(Path(__file__).parent / "vars.env")


@pytest.fixture(name="no_retry_sleep_fixture", autouse=True)
def no_retry_sleep() -> Generator[None]:
    """Strip the backoff so retry tests don't actually sleep."""
    original = repositories.PizzaPlatformAPI.read_pizzerias.retry.wait
    repositories.PizzaPlatformAPI.read_pizzerias.retry.wait = wait_none()
    yield
    repositories.PizzaPlatformAPI.read_pizzerias.retry.wait = original
