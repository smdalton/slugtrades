# Management extension for django commands
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.management import call_command
from slug_trade_app import models

from faker import Faker
import random
import os, sys
from django.core.files import File
from time import sleep
fake = Faker()

class Command(BaseCommand):


    fake.seed(4321)
    random.seed(4321)
    num_users = 10
    profile_data = [(fake.name(), fake.text(), random.choice(['on', 'off'])) for counter in range(num_users)]

        # Todo get the photos directory
    help = 'This is a customized command accessible from manage.py'
    print('calling populate db with  manage.py')

    # creates admin account and saves it
    def generate_date(self):
        return


    def create_admin(self):

        # Operations on user object
        user = User.objects.create_user('admin', password='pass1234')
        user.is_superuser = True
        user.is_staff = True
        user.first_name = 'admin'
        user.last_name = 'istrator'
        # userprofile fields
        user.save()

        # Operations
        user.userprofile.bio = 'This is a test bio for admin'
        # TODO://
        counter = 0
        # When looking at the project from the point of view of your system's root directory
        pwd = os.getcwd()
        # when looking in from top level of project, this is where the profile pics are at
        relative_dir = 'slug_trade/media/db_populate/profile_pics'
        # pick a specific
        filename = os.listdir(os.path.join(pwd, relative_dir))[counter]
        user.userprofile.on_off_campus = random.choice(['on', 'off'])
        full_path = os.path.join(pwd, relative_dir, filename)
        print(full_path)
        user.userprofile.profile_picture.save(user.first_name, File(open(full_path, 'rb')))
        user.userprofile.save()
        return

    def create_single_user(self):

        user = User.objects.create_user('')
        return
    def dir_print(self):
        print("\n\n ===========current Dir is {0} ===========\n".format(
            os.getcwd()
        ))
        print(os.listdir(os.getcwd()))

    def get_photos(self):
        self.dir_print()
        # switch directories to the place with the photos
        os.chdir(os.path.join(os.getcwd(), 'slug_trade/media/db_populate/profile_pics'))
        profile = os.listdir(os.getcwd())
        print("files for profile pics", profile[0])



    def wipe_db(self):
        call_command('flush')
        sleep(.3)
        sys.stdout.write('yes\n')

    def create_single_item(self):
        return

    def handle(self, **args):
        test = False
        # test = True
        # wipe the db
        if test:
            self.get_photos()

        else:
            self.wipe_db()
            self.create_admin()
            self.stdout.write('This worked, you nuked the db and started over')
            self.stdout.write('flushed')

