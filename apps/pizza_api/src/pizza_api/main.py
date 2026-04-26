"""Main entry point for the pizza API."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from pizza_api.dependencies.engine import create_engine
from pizza_api.routers import categories
from pizza_api import settings


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
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

app.include_router(categories.router)

# # create an app with a title and description
# if os.getenv("FUNCTIONS_WORKER_RUNTIME"):
#     app = FastAPI(
#         servers=[{"url": f"/api/{settings.name}", "description": "API"}],
#         root_path=f"/{settings.name}",
#         root_path_in_servers=False,
#         title=settings.title,
#         description=settings.description,
#         swagger_ui_oauth2_redirect_url="/oauth2-redirect",
#         swagger_ui_init_oauth={
#             "usePkceWithAuthorizationCodeGrant": True,
#             "clientId": auth_settings.open_api_client_id,
#             "scopes": auth_settings.scope_name,
#         },
#     )
# else:
#     app_auth_init = {}
#     if auth_settings.is_set:
#         app_auth_init["swagger_ui_oauth2_redirect_url"] = "/oauth2-redirect"
#         app_auth_init["swagger_ui_init_oauth"] = {
#             "usePkceWithAuthorizationCodeGrant": True,
#             "clientId": auth_settings.open_api_client_id,
#             "scopes": auth_settings.scope_name,
#         }
#     app = FastAPI(
#         title=f"{settings.title} - development",
#         description=settings.description,
#         **app_auth_init,
#     )

# # add GZipMiddleware in case of large payloads
# app.add_middleware(GZipMiddleware)

# # Include our hello world router
# app.include_router(router)