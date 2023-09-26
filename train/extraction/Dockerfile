FROM python:3.10.11
RUN pip install peotry
COPY pyproject.toml poetry.lock ./
#RUN poetry install
RUN poetry export --without-hashes --format=requirements.txt > requirements.txt
RUN cat requirements.txt
RUN pip install -r requirements.txt --no-cache-dir
CMD ["bash"]
