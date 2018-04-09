from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

ITEM_CATEGORIES = (
    ('E','Electronics'),
    ('H','Household goods'),
    ('C','Clothing'),
    ('O', 'Other')
)

CAMPUS_STATUS = (
    ('on', 'Located on campus'),
    ('off', 'Located off campus')
)



class Item(models.Model):
    # who owns the item
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    category = models.CharField(max_length=1,
                                default="O",
                                choices=ITEM_CATEGORIES)
    image = models.ImageField(upload_to='item_pictures')


#
# class Picture(models.Model):
#     item = models.ForeignKey(Item, on_delete=models.CASCADE)
#     picture = models.ImageField(upload_to='profile_optional', blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_picture')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=3,
                                default="on",
                                choices=CAMPUS_STATUS)

# These are needed to ensure auto creation of the other
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Offer(models.Model):
    bid_on = models.ForeignKey(Item, related_name='item_bid_on', on_delete=models.CASCADE)
    bid_with = models.ForeignKey(Item, related_name='item_bid_with', on_delete=models.CASCADE)


