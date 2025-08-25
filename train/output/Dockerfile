FROM python:3.10.15 AS builder
WORKDIR /app
SHELL ["/bin/bash", "-lc"]
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

COPY pyproject.toml uv.lock* ./
COPY train/output/pyproject.toml train/output/pyproject.toml

WORKDIR /app/train/output
RUN uv sync --no-dev

COPY train/output/ ./

FROM python:3.10.15-slim AS final
WORKDIR /app
RUN useradd -r newuser
COPY --from=builder /app/train/output/.venv /app/.venv
COPY --from=builder /app/train/output/ ./
USER newuser
ENV PATH="/app/.venv/bin:${PATH}"
