#!/usr/bin/env bash

source env/bin/activate
python3 manage.py flush --no-input
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py populate_db

