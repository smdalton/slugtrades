# Management extension for django commands
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.management import call_command
from slug_trade_app import models
from itertools import cycle

from faker import Faker
import random
import os, sys
from django.core.files import File
from time import sleep
fake = Faker()


class Command(BaseCommand):
    debug = True
    fake.seed(4321)
    random.seed(4321)
    num_users = 12
    # name, bio, on/off


    profile_pic_dir = 'slug_trade/media/db_populate/profile_pics'
        # Todo get the photos directory
    item_pic_dir = 'slug_trade/media/db_populate/item_pics'
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
        user.userprofile.bio = 'This is a test bio for admin, I chose this photo because this is what I feel like inside\n' \
                               'after having been in college for like 9 years'
        # TODO://
        counter = 0
        #
        filename = os.listdir(os.path.join(os.getcwd(), self.profile_pic_dir))[counter]
        user.userprofile.on_off_campus = random.choice(['on', 'off'])
        full_path = os.path.join(os.getcwd(), self.profile_pic_dir, filename)
        print(full_path)
        user.userprofile.profile_picture.save(user.first_name, File(open(full_path, 'rb')))
        user.userprofile.save()
        return

    def create_users(self):
        # profile data contains all of the fake information
        profile_data = [(fake.name(), fake.text(), random.choice(['on', 'off']), counter) for counter in range(self.num_users)]

        for name, bio, location, counter in profile_data:
            user = User.objects.create_user(username=name,
                                            email=''.join((name+'@somewhere.com').split(' ')).lower(),
                                            password='pass1234')
            user.email
            user.is_superuser = False
            user.is_staff = False
            user.first_name = name.split(' ')[0]
            user.last_name = name.split(' ')[1]
            user.save()
            user.userprofile.bio = bio
            if self.debug: print('setting location', location)
            user.userprofile.on_off_campus = location
            filename = os.listdir(os.path.join(os.getcwd(), self.profile_pic_dir))[counter]
            full_path = os.path.join(os.getcwd(), self.profile_pic_dir, filename)
            user.userprofile.profile_picture.save(user.first_name, File(open(full_path, 'rb')))
            user.userprofile.save()

    def create_item(self):
        # assign one item per user at this point in time

        # get a random user, assign them to the item
        # list all of the users
        user = User.objects.get(first_name='admin')
        item = models.Item(user=user, name='test', price='5.99', category='C', description='placeholder')
        item.save()
        filename = os.listdir(os.path.join(os.getcwd(), self.item_pic_dir))[0]
        full_path = os.path.join(os.getcwd(), self.item_pic_dir, filename)
        image = models.ItemImage(item=item)
        image.image1.save('admin', File(open(full_path,'rb')))
        image.save()
        #print(image)

    def create_items(self):

        # create a cycle of all of the users of the database
        print('all of the users:')
        from_user_list = cycle([user for user in User.objects.all()])
        pictures_list = [item for item in os.listdir(os.path.join(os.getcwd(), self.item_pic_dir)) if not item.startswith('.')]
        item_names = [picture.split(' ')[0] for picture in pictures_list if not picture.startswith('.')]

        # pictures list:
        for picture in pictures_list:
            user = next(from_user_list)
            picture_name = picture.split('.')[0]
            item = models.Item(user=user, name=picture_name, price=random.random()*100, category='C', description=fake.text())
            item.save()
            full_path = os.path.join(os.getcwd(), self.item_pic_dir, picture)
            image = models.ItemImage(item=item)
            image.image1.save(picture_name, File(open(full_path, 'rb')))
            image.save()
        # for picture in pictures get the picture path and filename from the list of all the pictures in pics directory

        # get a random user
        # create the item, naming it with the filename
        # generate a random price ( or no price at all )
        #
        #

        # create the base item with some default values
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
        self.stdout.write('DB has been flushed')

    def create_single_item(self):
        # make a bike first
        item = models.Item()


        return

    def handle(self, **args):
        test = False
        #test = True
        # wipe the db
        if test:
            # test functions go in here
            self.create_item()
            self.wipe_db()
            self.stdout.write('flushed')
            self.create_admin()
            self.create_users()
            self.create_items()

        else:
            self.create_item()
            self.wipe_db()
            self.stdout.write('flushed')
            self.create_admin()
            self.create_users()
            self.create_items()


