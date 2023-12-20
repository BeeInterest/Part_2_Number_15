FROM python:3.10

WORKDIR /db
RUN pip install --no-cache-dir --upgrade pip
RUN pip install mimesis
RUN pip install faker
RUN apk add --no-cache gcc musl-dev
COPY . /db