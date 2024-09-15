FROM python:3.10.13 AS base

FROM base AS builder

WORKDIR /app

ENV PATH=/root/.local/bin:$PATH \
    POETRY_VERSION=1.8.3

RUN pip install --user "poetry==${POETRY_VERSION}"
RUN python -m venv /venv

COPY ./ ./

RUN ls -la

# --sync            Synchronize the environment with the locked packages and the specified groups
# --no-directory    Do not install any directory path dependencies; useful to install dependencies without source code
# -n                Do not ask any interactive question.
RUN . /venv/bin/activate && poetry install -n --sync --no-directory --no-root


FROM base AS final
RUN useradd -r newuser
USER newuser
ENV PATH=/venv/bin:${PATH}

COPY --from=builder /venv /venv