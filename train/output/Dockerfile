FROM python:3.10.13

COPY pyproject.toml .
COPY poetry.lock .

RUN python -m pip install --upgrade pip
RUN python -m pip install poetry --user
RUN python -m poetry export --format=requirements.txt > requirements.txt
RUN python -m pip install -r requirements.txt --no-cache-dir

CMD ["bash"]
