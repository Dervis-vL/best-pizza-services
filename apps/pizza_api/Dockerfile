FROM python:3.13-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

# Copy workspace first; this layer is cached unless deps change
COPY pyproject.toml uv.lock ./
COPY apps/pizza_api/pyproject.toml apps/pizza_api/pyproject.toml
COPY apps/pizza_app/pyproject.toml apps/pizza_app/pyproject.toml
COPY packages/pizza_platform_shared/pyproject.toml packages/pizza_platform_shared/pyproject.toml
COPY services/pizza_data_collector/pyproject.toml services/pizza_data_collector/pyproject.toml
COPY services/pizza_data_storage/pyproject.toml services/pizza_data_storage/pyproject.toml
COPY services/geolocation/pyproject.toml services/geolocation/pyproject.toml

# Install external dependencies without the workspace packages themselves
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --package pizza_api --no-dev --frozen --no-install-workspace

# Copy only the source trees needed by pizza_api and its workspace deps
COPY apps/pizza_api/src apps/pizza_api/src
COPY packages/pizza_platform_shared/src packages/pizza_platform_shared/src
COPY services/pizza_data_collector/src services/pizza_data_collector/src
COPY services/pizza_data_storage/src services/pizza_data_storage/src
COPY services/geolocation/src services/geolocation/src

# Install workspace packages as non-editable wheels so only .venv is needed at runtime
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --package pizza_api --no-dev --locked --no-editable


FROM python:3.13-slim AS production

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

RUN groupadd --system appgroup && \
    useradd --system --gid appgroup --no-create-home appuser

USER appuser

EXPOSE 8000

CMD ["uvicorn", "pizza_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
