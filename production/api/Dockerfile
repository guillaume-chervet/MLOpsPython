FROM python:3.10.13

WORKDIR /app
COPY . /app

ENV PATH=/root/.local/bin:$PATH \
    POETRY_VERSION=1.8.3

RUN pip install --user "poetry==${POETRY_VERSION}"
RUN python -m venv /venv
RUN pip install poetry && poetry install --no-root --only main

# --sync            Synchronize the environment with the locked packages and the specified groups
# --no-directory    Do not install any directory path dependencies; useful to install dependencies without source code
# -n                Do not ask any interactive question.
RUN . /venv/bin/activate && poetry install -n --sync --no-directory --no-root

ENV PATH=/venv/bin:${PATH}

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]