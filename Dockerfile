FROM python:3.7

ENV DEBUG=false
ENV DJANGO_SETTINGS_MODULE=config.settings.production

WORKDIR /app

RUN set -ex \
    && pip install poetry \
    && poetry --version

COPY pyproject.toml .
COPY poetry.lock    .

RUN set -ex \
    && poetry install

COPY ./scripts/docker-entrypoint.sh /usr/local/bin/
RUN set -ex \
    && chmod +x /usr/local/bin/docker-entrypoint.sh

COPY . .

EXPOSE 8000

ENTRYPOINT ["docker-entrypoint.sh"]
