FROM python:3.13-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Copy workspace manifests first — this layer is cached unless deps change
COPY pyproject.toml uv.lock ./
COPY apps/pizza_api/pyproject.toml apps/pizza_api/pyproject.toml
COPY apps/pizza_app/pyproject.toml apps/pizza_app/pyproject.toml
COPY packages/pizza_platform_shared/pyproject.toml packages/pizza_platform_shared/pyproject.toml
COPY services/pizza_data_collector/pyproject.toml services/pizza_data_collector/pyproject.toml
COPY services/pizza_data_storage/pyproject.toml services/pizza_data_storage/pyproject.toml
COPY services/geolocation/pyproject.toml services/geolocation/pyproject.toml

# Install all external dependencies without the workspace packages themselves
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --package pizza_app --no-dev --frozen --no-install-project

# Copy only the source trees needed by pizza_app and its workspace deps
COPY apps/pizza_app/src apps/pizza_app/src
COPY packages/pizza_platform_shared/src packages/pizza_platform_shared/src

# Install workspace packages as non-editable wheels so only .venv is needed at runtime
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --package pizza_app --no-dev --frozen --no-editable


FROM python:3.13-slim AS production

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN groupadd --system appgroup && \
    useradd --system --gid appgroup --no-create-home appuser

USER appuser

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')"

# os.execlp replaces the Python process with streamlit (clean PID 1 behaviour)
CMD ["python", "-c", "import pizza_app, os; app=os.path.join(os.path.dirname(pizza_app.__file__), 'app.py'); os.execlp('streamlit', 'streamlit', 'run', app, '--server.port=8501', '--server.address=0.0.0.0', '--server.headless=true')"]
