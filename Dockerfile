FROM python:3.6

WORKDIR /app

RUN set -ex \
    && pip install poetry \
    && poetry --version