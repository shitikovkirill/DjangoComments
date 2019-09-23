#!/bin/bash

if [[ "$DEBUG" = "true" ]]
then
    set -ex
fi

until PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

if [[ "$@" = "bash" ]]
then
    poetry shell
    exec "$@"
else
    poetry run "$@"
fi
