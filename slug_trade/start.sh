#!/usr/bin/env bash

sh venv_setup.sh
source env/bin/activate
find slug_trade_app/migrations "*auto*.py" -not -name "__init__.py" -delete
rm db.sqlite3
sh renew_db.sh
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --no-input
python3 manage.py runserver 0.0.0.0:8000
