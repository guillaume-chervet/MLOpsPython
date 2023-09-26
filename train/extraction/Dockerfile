FROM python:3.10.11
COPY requirements.txt ./
RUN mkdir packages
COPY packages/ packages/
RUN ls packages/
RUN pip install -r requirements.txt --no-cache-dir
CMD ["bash"]
