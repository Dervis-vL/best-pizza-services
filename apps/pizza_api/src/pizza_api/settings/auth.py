"""Auth settings for pizza_api."""

from typing import Annotated

import pydantic as pyd
import pydantic_settings as pyd_settings
from pydantic import computed_field


class AuthSettings(pyd_settings.BaseSettings):
    """Authentication settings for the pizza API."""

    open_api_client_id: Annotated[
        str,
        pyd.Field(
            description="The client ID.",
        ),
    ] = ""
    app_client_id: Annotated[
        str,
        pyd.Field(
            description="The client ID of the API.",
        ),
    ] = ""
    tenant_id: Annotated[
        str,
        pyd.Field(
            description="The tenant ID of company.",
        ),
    ] = ""
    scope_description: Annotated[
        str,
        pyd.Field(
            description="The scope description of the API.",
        ),
    ] = "user_impersonation"

    @property
    @computed_field
    def is_set(self) -> bool:
        """Return True if all required auth settings are set, False otherwise."""
        return bool(self.open_api_client_id and self.app_client_id and self.tenant_id)

    @property
    @computed_field
    def scope_name(self) -> str:
        """Return the scope name for the API, which is used in documentation."""
        return f"api://{self.app_client_id}/{self.scope_description}"

    @property
    @computed_field
    def scopes(self) -> dict[str, str]:
        """Return the scopes dict for the API, which is used in documentation."""
        return {self.scope_name: self.scope_description}
