FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10
WORKDIR /app

COPY . .
RUN python -m pip install --no-cache-dir --upgrade  -r requirements.txt
ENV PATH ${APP_ROOT}/.local/bin:${PATH}
CMD ["python", "index.py"]
