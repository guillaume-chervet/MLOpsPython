FROM python:3.10 AS builder

ENV DEBIAN_FRONTEND=noninteractive \
    VIRTUAL_ENV=/opt/venv \
    UV_HTTP_TIMEOUT=300

RUN python -m pip install -U pip && pip install uv

RUN uv venv "$VIRTUAL_ENV"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /workspace

COPY . /workspace/projects/step

COPY mlopspython-extraction /workspace/packages/mlopspython-extraction
WORKDIR /workspace/projects/step
RUN uv sync --no-editable --frozen

FROM python:3.10 AS final
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV

WORKDIR /app
COPY --from=builder /workspace/projects/step ./
ENV UV_HTTP_TIMEOUT=300

RUN useradd -r appuser
USER appuser


