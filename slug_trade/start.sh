#!/usr/bin/env bash

source env/bin/activate
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:80
