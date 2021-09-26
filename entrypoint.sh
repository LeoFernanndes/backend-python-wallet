#!/bin/sh
python manage.py collectstatic --no-input
python manage.py makemigrations cashback people products
python manage.py migrate
gunicorn backend_python_wallet.wsgi:application --bind 0.0.0.0:8000 --workers 3 --access-logfile='-'
exec "$@"