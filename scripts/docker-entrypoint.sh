#!/bin/bash

if [[ "$DEBUG" = "true" ]]
then
    set -ex
fi

if [[ "$@" = "bash" ]]
then
    exec "$@"
else
    poetry run "$@"
fi