#!/bin/sh
python manage.py makemigrations

python manage.py migrate

python manage.py collectstatic --noinput

cp -r collected_static/. /backend_static/static/

DJANGO_SUPERUSER_EMAIL="admin@admin.com" \
DJANGO_SUPERUSER_USERNAME=admin \
DJANGO_SUPERUSER_PASSWORD=admin \
DJANGO_SUPERUSER_FIRST_NAME=admin \
DJANGO_SUPERUSER_LAST_NAME=admin \
DJANGO_SUPERUSER_PHONE="8(999)adm-in-im" \
python manage.py createsuperuser --noinput

gunicorn --reload -b 0.0.0.0:8000 ambassadors_project.wsgi
