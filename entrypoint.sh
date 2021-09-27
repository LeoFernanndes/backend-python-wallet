#!/bin/sh
python manage.py collectstatic --no-input
python manage.py makemigrations cashback people products
python manage.py migrate
python manage.py loaddata users product_types  customers products cashbacks
gunicorn backend_python_wallet.wsgi:application --bind 0.0.0.0:8000 --workers 3 --access-logfile='-'
exec "$@"