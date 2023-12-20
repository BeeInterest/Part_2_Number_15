FROM python:3.10

WORKDIR /db
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN apk add --no-cache gcc musl-dev
COPY . /db