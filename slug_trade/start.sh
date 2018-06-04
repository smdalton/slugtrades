#!/usr/bin/env bash

source env/bin/activate
./renew_db.sh
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
