#!/bin/sh

echo "Waiting fro PostgreSQL in user-db:5432..."

while ! nc -z db 5432; do
  sleep 1
done

echo "PostgreSQL inited"

python manage.py makemigrations
python manage.py migrate

exec "$@"