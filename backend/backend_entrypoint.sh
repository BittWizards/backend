#!/bin/sh
python manage.py makemigrations

python manage.py migrate

python manage.py collectstatic

cp -r collected_static/. /collected_static/

DJANGO_SUPERUSER_PASSWORD=admin \
DJANGO_SUPERUSER_USERNAME=admin \
DJANGO_SUPERUSER_EMAIL="admin@admin.com" \
python manage.py createsuperuser --noinput

python manage.py loaddata */fixtures/*.json

gunicorn --reload -b 0.0.0.0:8000 ambassadors_project.wsgi
