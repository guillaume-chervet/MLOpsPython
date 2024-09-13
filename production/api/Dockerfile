FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10
WORKDIR /app

COPY . .

ENV POETRY_VERSION=1.8.3

RUN python -m pip install --upgrade pip
RUN python -m pip install --user "poetry==${POETRY_VERSION}"
RUN python -m poetry install -n --sync --no-directory --no-root

CMD ["python", "-m", "poetry", "run", "python", "index.py"]
