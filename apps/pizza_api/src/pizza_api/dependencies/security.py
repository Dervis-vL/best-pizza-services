"""Security dependencies for the pizza API."""

from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from pizza_api import settings

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_api_key(key: Annotated[str | None, Security(_api_key_header)]) -> None:
    """Require a valid API key for access to the endpoint."""
    expected = settings.app_settings.key.get_secret_value()
    if not expected or key != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
        )


RequireApiKeyDep = Annotated[None, Depends(require_api_key)]
