#!/usr/bin/env python
import os
import sys
from django.db.utils import IntegrityError

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "slug_trade.settings")

    from django.core.management import execute_from_command_line
    try:
        execute_from_command_line(sys.argv)
    except IntegrityError as e:
        print(e)
        pass