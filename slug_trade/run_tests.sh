#!/usr/bin/env bash

source env/bin/activate
PATH=./tests/:$PATH
python3 tests/test_title.py
# python3 tests/test_login.py
