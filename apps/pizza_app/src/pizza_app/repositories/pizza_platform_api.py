"""Data access layer; read pizzeeria data from the API."""

import logging

import requests
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from pizza_app import constants, exceptions, settings
from pizza_app.settings.pizza_api import PizzaAPISettings
from pizza_platform_shared import constants as shared_consts
from pizza_platform_shared import schemas as shared_schemas

logger = logging.getLogger(__name__)


class PizzaPlatformAPI:
    """Reads pizzeria location data from the pizza platform API."""

    def __init__(self, api_settings: PizzaAPISettings) -> None:
        """Initialize the API client.

        Args:
            api_settings: Resolved API settings

        """
        self.api_settings = api_settings

    @retry(
        stop=stop_after_attempt(settings.retry_api.max_attempts),
        wait=wait_random_exponential(
            multiplier=settings.retry_api.backoff_base,
            max=settings.retry_api.backoff_max,
        ),
        retry=retry_if_exception_type(exceptions.TransientAPIError),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
    def read_pizzerias(self) -> list[shared_schemas.PizzeriaReadSchema]:
        """Read pizzeria location data from the API, retrying transient failures."""
        # HTTP request using the settings url here with timeout and error handling
        try:
            response = requests.get(
                f"{self.api_settings.base_url}{constants.PizzaAPI.PIZZERIAS_ENDPOINT}",
                timeout=constants.PizzaAPI.TIMEOUT,
            )
        except (requests.ConnectionError, requests.Timeout) as e:
            msg = f"Pizza platform API unreachable: {e}"
            raise exceptions.TransientAPIError(msg) from e

        if response.status_code in shared_consts.RETRYABLE_STATUS:
            msg = f"Pizza platform API returned HTTP {response.status_code}"
            raise exceptions.TransientAPIError(msg)

        response.raise_for_status()  # 4xx etc. no retry, raise for caller to handle
        return [shared_schemas.PizzeriaReadSchema(**pizzeria) for pizzeria in response.json()]
