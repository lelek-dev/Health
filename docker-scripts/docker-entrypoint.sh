#!/usr/bin/env bash
/usr/local/bin/wait-for-it.sh db:5432
python manage.py makemigrations
python manage.py migrate

exec "$@"