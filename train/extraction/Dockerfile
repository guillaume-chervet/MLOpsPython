FROM python:3.10.13
COPY requirements.txt ./
RUN mkdir packages
COPY packages/ packages/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
CMD ["bash"]
