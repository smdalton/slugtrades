#!/usr/bin/env bash

source env/bin/activate
PATH=./tests/:$PATH
python3 tests/test_logo_loads.py
python3 tests/test_login_and_logout.py
