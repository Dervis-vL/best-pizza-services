"""Router for health check endpoint."""

from fastapi import APIRouter, status

router = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, str],
    summary="Health check endpoint.",
)
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
