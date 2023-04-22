#!/bin/bash
python manage.py makemigrations --no-input
python manage.py collectstatic --no-input
python manage.py migrate
celery --app=core worker --loglevel=info --concurrency 4 -P eventlet  --uid=0 --gid=0 &
#gunicorn --log-level=debug core.wsgi
#celery flower -A core --port=5555 --broker=redis://default:xP6JtBIJS2MAPfoLMxZS@containers-us-west-48.railway.app:7317
