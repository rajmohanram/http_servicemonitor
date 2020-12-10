#!/bin/sh
set -e

crond -b -L /dev/stdout
python manage.py crontab add
python manage.py runserver 0.0.0.0:8000