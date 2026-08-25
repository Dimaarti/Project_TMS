#!/bin/sh

set -e

echo "applying database migrations"
python src/manage.py migrations --noinput

echo "collecting static files"
python src/manage.py collectstatic --noinput

echo "starting gunicorn"
exec python -m gunicorn \
    --chdir src \
    --bind 0.0.0.0:8000 \
    --workers 1 \
    --timeout 120 \
    --access-loglife - \
    --error-loglife - \
    config.wsgi:application