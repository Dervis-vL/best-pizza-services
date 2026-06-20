"""Main entry point for the pizza API."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Final

from fastapi import Depends, FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from pizza_api import constants, routers, settings
from pizza_api.dependencies.engine import create_engine
from pizza_api.dependencies.security import require_api_key


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None]:
    """Create the shared DB engine on startup and dispose it on shutdown."""
    application.state.engine = create_engine()
    yield
    application.state.engine.dispose()


app = FastAPI(
    title=settings.app_settings.title,
    description=settings.app_settings.description,
    version=settings.app_settings.version,
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
)

app.mount(
    constants.ApiConstants.STATIC_URL,
    StaticFiles(directory=constants.ApiConstants.STATIC_DIR),
    name="static",
)

app.include_router(routers.categories.router, dependencies=[Depends(require_api_key)])
app.include_router(routers.maintenance.router, dependencies=[Depends(require_api_key)])
app.include_router(routers.pizzerias.router)
app.include_router(routers.health.router)


_OPENAPI_URL: Final[str] = app.openapi_url or "/openapi.json"
_OAUTH2_REDIRECT_URL: Final[str] = app.swagger_ui_oauth2_redirect_url or "/docs/oauth2-redirect"


@app.get("/docs", include_in_schema=False)
async def swagger_ui_html() -> HTMLResponse:
    """Serve Swagger UI with a custom favicon."""
    return get_swagger_ui_html(
        openapi_url=_OPENAPI_URL,
        title=f"{app.title} - Swagger UI",
        oauth2_redirect_url=_OAUTH2_REDIRECT_URL,
        swagger_favicon_url=constants.ApiConstants.FAVICON_URL,
    )


@app.get(_OAUTH2_REDIRECT_URL, include_in_schema=False)
async def swagger_ui_redirect() -> HTMLResponse:
    """Serve the Swagger UI OAuth2 redirect page."""
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html() -> HTMLResponse:
    """Serve ReDoc with a custom favicon."""
    return get_redoc_html(
        openapi_url=_OPENAPI_URL,
        title=f"{app.title} - ReDoc",
        redoc_favicon_url=constants.ApiConstants.FAVICON_URL,
    )
