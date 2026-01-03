"""Settings for the source location to be scraped."""

import urllib
from typing import Annotated

import pydantic
import pydantic_settings


class SourcePageSettings(pydantic_settings.BaseSettings):
    """Settings for the source webpage location to be scraped."""

    url_home: Annotated[
        urllib.URL, pydantic.Field(
            description="The URL of the source to be scraped."
        ),
    ] = urllib.URL("https://www.50toppizza.it/")
    selection_type: Annotated[
        str,
        pydantic.Field(
            description="The type of selection to be made on the source page."
        ),
    ] = "50-top"


    class Config:
        """Configuration for SourceSettings."""

        env_prefix = "SOURCE_"
        case_sensitive = False