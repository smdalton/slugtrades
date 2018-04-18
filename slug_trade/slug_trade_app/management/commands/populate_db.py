# Management extension for django commands
from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'This is a customized command accessible from manage.py'
    print('calling populate db with  manage.py')

    def handle(self, **args):
        self.stdout.write('This shit worked')

