FROM python:3.11.1

RUN pip install pipenv

#ENV PROJECT_DIR /usr/local/src/webapp

#WORKDIR ${PROJECT_DIR}

#COPY Pipfile Pipfile.lock ${PROJECT_DIR}/
COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy

RUN pipenv lock -r > requirements.txt
RUN cat requirements.txt

RUN pip install -r requirements.txt --no-cache-dir

CMD ["bash"]