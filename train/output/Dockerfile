FROM python:3.11 AS base

FROM base AS builder

WORKDIR /app

RUN pip install uv

COPY ./ /app/

RUN uv venv
RUN . .venv/bin/activate

RUN export UV_HTTP_TIMEOUT=300 && uv sync --no-editable


FROM base AS final
RUN useradd -r newuser
USER newuser
ENV PATH=/.venv/bin:${PATH}

COPY --from=builder /app/.venv /.venv
