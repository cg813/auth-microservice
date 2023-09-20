#!/bin/sh

echo "Waiting for mongo..."

while ! nc -z auth-mongo-srv 27017; do
  sleep 0.1
done

echo "MongoDB started"

exec "$@"