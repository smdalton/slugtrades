#!/usr/bin/env bash

python3 -m virtualenv env

pip install -r requirements.txt
sleep 1
source env/bin/activate
