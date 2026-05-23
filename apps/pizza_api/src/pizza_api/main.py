"""Main entry point for the pizza API."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from pizza_api import routers, settings
from pizza_api.dependencies.engine import create_engine


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
)

app.include_router(routers.categories.router)
app.include_router(routers.maintenance.router)
app.include_router(routers.pizzerias.router)
