# Management extension for django commands
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.management import call_command

from slug_trade_app import models
from itertools import cycle
from faker import Faker
import random
import os, sys

# Modules for image handling
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
import glob


fake = Faker()

class Command(BaseCommand):
    help = 'This is a customized command accessible from manage.py'

    debug = True
    fake.seed(4321)
    random.seed(4321)
    num_users = 12

    debug_profile_pic_path = os.path.join(os.getcwd(), 'slug_trade/media/db_populate/profile_pics/')
    debug_item_pic_path = os.path.join(os.getcwd(), 'slug_trade/media/db_populate/item_pics/')

# Creates admin account and saves it into the database.
    def create_admin(self):
        # Create admin user.
        user = User.objects.create_user('admin', password='pass1234')
        user.is_superuser = True
        user.is_staff = True
        user.first_name = 'admin'
        user.last_name = 'istrator'
        user.email = 'admin@email.com'
        user.save()

        profile = models.UserProfile(user=user)
        profile.save()

        user.userprofile.bio = 'This is a bio for the admin user,  whose first name is admin and ' \
                               'last name is istrator, who has no email address, and lives off campus.'
        user.userprofile.on_off_campus = 'off'

        # get the debug image to use as the profile photo
        filename = glob.glob(self.debug_profile_pic_path + 'debug.jpeg')[0]
        extension = '.' + filename.split('.')[len(filename.split('.'))-1]
        image = Image.open(filename)
        image_bytes = BytesIO()
        image.save(image_bytes, image.format)

        user.userprofile.profile_picture.save(user.first_name + extension, ContentFile(image_bytes.getvalue()))
        user.userprofile.save()

        return

# Creates one user and saves it into the database.
    def create_user(self):
        # Create debug user information.
        name = 'Test User'
        bio = 'This is a bio for Test User,  whose first name is Test and ' \
              'last name is User, who has email address testuser@somewhere.com, and lives on campus.'
        location = 'on'

        username = name.replace(' ', '')
        user = User.objects.create_user(username=username.lower(), password='pass1234')
        user.is_superuser = False
        user.is_staff = False
        user.first_name = name.split(' ')[0]
        user.last_name = name.split(' ')[1]
        user.email = (username + '@somewhere.com').lower()
        user.save()

        profile = models.UserProfile(user=user)
        profile.save()

        user.userprofile.bio = bio
        user.userprofile.on_off_campus = location

        # get the debug image to use as the profile photo
        filename = glob.glob(self.debug_profile_pic_path + 'debug.jpeg')[0]
        extension = '.' + filename.split('.')[len(filename.split('.'))-1]
        image = Image.open(filename)
        image_bytes = BytesIO()
        image.save(image_bytes, image.format)

        user.userprofile.profile_picture.save(user.first_name + extension, ContentFile(image_bytes.getvalue()))
        user.userprofile.save()

        return

# Creates number of users specified in class declaration, populates the fields with random information, and saves them into the database.
    def create_random_users(self):
        image_list = glob.glob(self.debug_profile_pic_path + 'images-*.jpeg')

        # profile data contains all of the fake information
        profile_data = [(fake.name(), fake.text(), random.choice(['on', 'off']), counter) for counter in range(self.num_users)]

        for name, bio, location, counter in profile_data:
            username = name.replace(' ', '')
            user = User.objects.create_user(username=username.lower(), password='pass1234')
            user.is_superuser = False
            user.is_staff = False
            user.first_name = name.split(' ')[0]
            user.last_name = name.split(' ')[1]
            user.email = (username + '@somewhere.com').lower()
            user.save()

            profile = models.UserProfile(user=user)
            profile.save()

            user.userprofile.bio = bio
            user.userprofile.on_off_campus = location

            # get an image to use as the profile photo
            filename = image_list[counter % len(image_list)]
            extension = '.' + filename.split('.')[len(filename.split('.'))-1]
            image = Image.open(filename)
            image_bytes = BytesIO()
            image.save(image_bytes, image.format)

            user.userprofile.profile_picture.save(user.first_name + extension, ContentFile(image_bytes.getvalue()))
            user.userprofile.save()

        return

# Create one debug item for the user 'admin' and save it into the database.
    def create_admin_item(self):
        # get the user 'admin'
        user = User.objects.get(first_name='admin')

        # create the debug item
        item = models.Item(user=user, name='test', price='5.99', category='C', description='placeholder')
        item.save()

        # get the debug image to use as the item image
        filename = glob.glob(self.debug_item_pic_path + 'debug.jpeg')[0]
        extension = '.' + filename.split('.')[len(filename.split('.'))-1]
        image = Image.open(filename)
        image_bytes = BytesIO()
        image.save(image_bytes, image.format)

        modelimage = models.ItemImage(item=item)
        modelimage.image1.save('admin' + extension, ContentFile(image_bytes.getvalue()))
        modelimage.save()

        return

    def create_one_item_per_user(self):
        # create a cycle of all of the users of the database
        from_user_list = cycle([user for user in User.objects.all()])

        # get all of the debug item pictures
        file_list = os.listdir(self.debug_item_pic_path)
        pictures_list = [item for item in file_list]

        TRADE_OPTIONS = (
            ('0','Cash Only'),
            ('1','Cash with items on top'),
            ('2','Trade only'),
            ('3','Free')
        )
        # create a random debug item for each image
        for picture in pictures_list:
            user = next(from_user_list)
            picture_name = picture.split('.')[0]
            item = models.Item(user=user,
                               name=picture_name,
                               price=random.random()*100,
                               category='C',
                               description=fake.text(),
                               trade_options=random.choice(['0','2','3']))
            item.save()

            # get the item image from its name
            filename = glob.glob(self.debug_item_pic_path + picture)[0]
            extension = '.' + filename.split('.')[len(filename.split('.'))-1]
            image = Image.open(filename)
            image_bytes = BytesIO()
            image.save(image_bytes, image.format)

            modelimage = models.ItemImage(item=item)
            modelimage.image1.save(picture_name + extension, ContentFile(image_bytes.getvalue()))
            modelimage.save()

        return

    def wipe_db(self):
        # delete table entries
        call_command('flush')

        # get the path of the profile and item images that are associated with database entries
        profile_path = os.path.join(os.getcwd(), 'slug_trade/media/static/profile_pictures/')
        item_path = os.path.join(os.getcwd(), 'slug_trade/media/static/item_images/')

        # create the directories if they don't already exist (git ignores empty directories)
        if not os.path.exists(profile_path):
            os.makedirs(profile_path)
        if not os.path.exists(item_path):
            os.makedirs(item_path)

        # delete the images
        for filename in os.listdir(profile_path):
            os.remove(profile_path + filename)
        for filename in os.listdir(item_path):
            os.remove(item_path + filename)

    def handle(self, **args):
        test = False
        #test = True

        self.wipe_db()
        self.create_admin()
        self.create_admin_item()
        self.create_user()
        self.create_random_users()
        self.create_one_item_per_user()

        #if test:
            #test functions go here
