FROM python:3.10.15 AS builder
WORKDIR /app
SHELL ["/bin/bash", "-lc"]
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Manifeste + deps locales
COPY pyproject.toml uv.lock* ./
COPY train/extraction/pyproject.toml train/extraction/pyproject.toml

WORKDIR /app/train/extraction
RUN uv sync --no-dev

# Code
COPY train/extraction/ ./

FROM python:3.10.15-slim AS final
WORKDIR /app
RUN useradd -r newuser
COPY --from=builder /app/train/extraction/.venv /app/.venv
COPY --from=builder /app/train/extraction/ ./
USER newuser
ENV PATH="/app/.venv/bin:${PATH}"
