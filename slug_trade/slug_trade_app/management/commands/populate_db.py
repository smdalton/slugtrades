# Management extension for django commands
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from . import models
from faker import Faker
import random

class Command(BaseCommand):


    fake = Faker()
    fake.seed(4321)
    num_users = 10
    profile_data = [(fake.name(), fake.text()) for counter in range(num_users)]

    help = 'This is a customized command accessible from manage.py'
    print('calling populate db with  manage.py')

    # creates admin account and saves it

    def create_admin(self):
        user = User.objects.create_user('admin', password='pass1234')
        user.is_superuser = True
        user.is_staff = True
        # userprofile fields
        user.userprofile.bio = 'This is a test bio for admin'
        # TODO://
        user.userprofile.profile_picture = ''
        choices = ['on', 'off']
        user.userprofile.on_off_campus = random.choice(['on','off'])
        user.save()
        return

    def create_single_user(self):

        user = User.objects.create_user('')
        return

    def create_single_item(self):
        return

    def handle(self, **args):
        self.create_admin()
        self.stdout.write('This shit worked')

