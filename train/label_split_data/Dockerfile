FROM python:3.10.15 AS builder
WORKDIR /app
SHELL ["/bin/bash", "-lc"]
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

COPY pyproject.toml uv.lock* ./
COPY train/label_split_data/pyproject.toml train/label_split_data/pyproject.toml

WORKDIR /app/train/label_split_data
RUN uv sync --no-dev

COPY train/label_split_data/ ./

FROM python:3.10.15-slim AS final
WORKDIR /app
RUN useradd -r newuser
COPY --from=builder /app/train/label_split_data/.venv /app/.venv
COPY --from=builder /app/train/label_split_data/ ./
USER newuser
ENV PATH="/app/.venv/bin:${PATH}"
