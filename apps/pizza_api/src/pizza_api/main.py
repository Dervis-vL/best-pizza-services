"""Main entry point for the pizza API."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from pizza_api.dependencies import create_engine
from pizza_api.routers import categories


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
    """Create the shared DB engine on startup and dispose it on shutdown."""
    application.state.engine = create_engine()
    yield
    application.state.engine.dispose()


app = FastAPI(
    title="Best Pizza API",
    description="API for managing and scraping pizza ranking data.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(categories.router)
