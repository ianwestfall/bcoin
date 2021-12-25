#!/usr/bin/env bash

python manage.py migrate

# Lol please don't do this in prod. Use gunicorn behind Nginx or something
python manage.py runserver 0.0.0.0:8000
