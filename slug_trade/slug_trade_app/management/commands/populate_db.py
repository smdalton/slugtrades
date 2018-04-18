# Management extension for django commands
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from . import models
from faker import Faker


class Command(BaseCommand):
    fake= Faker()
    help = 'This is a customized command accessible from manage.py'
    print('calling populate db with  manage.py')

    # create and admin account
    def create_admin(self):
        user = User.objects.create_user('admin', password='pass1234')
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return

    def create_users(self):
        return


    def create_items(self):
        return

    def handle(self, **args):
        self.create_admin()
        self.stdout.write('This shit worked')

