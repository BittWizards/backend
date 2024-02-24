#!/bin/sh
python manage.py makemigrations

python manage.py migrate

python manage.py collectstatic --noinput

cp -r collected_static/. /backend_static/static/

DJANGO_SUPERUSER_PASSWORD=admin \
DJANGO_SUPERUSER_USERNAME=admin \
DJANGO_SUPERUSER_EMAIL="admin@admin.com" \
python manage.py createsuperuser --noinput

gunicorn --reload -b 0.0.0.0:8000 ambassadors_project.wsgi & daphne -v 1 -b 0.0.0.0 -p 8001 ambassadors_project.asgi:application --access-log -
# daphne -v 1 -b 0.0.0.0 -p 8000 ambassadors_project.asgi:application --access-log -
