#!/usr/bin/env bash

if [ "$1" == "" ]; then
    echo "usage: pylint <file>"
    exit 1
fi

source env/bin/activate
ERR_C0111="--disable=C0111"    # C0111: missing-dosctring
ERR_C0103="--disable=C0103"    # C0103: invalid-name
pylint $ERR_C0111 $ERR_C0103 $1
