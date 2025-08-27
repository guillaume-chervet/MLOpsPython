FROM python:3.10.15 AS base

FROM base AS builder

WORKDIR /app
SHELL ["/bin/bash", "-lc"]
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

COPY pyproject.toml uv.lock* ./
RUN uv venv && source .venv/bin/activate && uv sync --no-dev

FROM base AS final
RUN useradd -r newuser
USER newuser
ENV PATH=/venv/bin:${PATH}

COPY --from=builder /venv /venv