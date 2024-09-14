FROM python:3.10.13

WORKDIR /app
COPY . /app
#COPY pyproject.toml poetry.lock /app/

RUN pip install poetry && poetry install --no-root --only main


EXPOSE 8000

CMD ["uvicorn", "index:app", "--host", "0.0.0.0", "--port", "5000"]