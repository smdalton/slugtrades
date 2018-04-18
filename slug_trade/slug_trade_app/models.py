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


TRADE_OPTIONS = (
    ('0','Cash Only'),
    ('1','Cash with items on top'),
    ('2','Trade only'),
    ('3','Free')
)


ITEM_CONDITION = (
    ('0','Well Loved'),
    ('1','Fair'),
    ('2','Good'),
    ('3','Like New'),
    ('3','New')
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='static/profile_pictures', blank=True )
    bio = models.TextField(max_length=500, blank=True)
    on_off_campus = models.CharField(max_length=3,
                                default="on",
                                choices=CAMPUS_STATUS)


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wishlist_item_description = models.CharField(max_length=1000, blank=False)


class Item(models.Model):
    # who owns the item
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, blank=False)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=False)
    category = models.CharField(max_length=1,
                                default="O",
                                choices=ITEM_CATEGORIES,
                                blank=False)
    trade_options = models.CharField(max_length=80,
                                     default='1',
                                    choices=TRADE_OPTIONS,
                                    blank=False)
    bid_counter = models.IntegerField(default=0, blank=False)
    description = models.TextField(blank=False, default=' ')
    condition = models.CharField(choices=ITEM_CONDITION,
                                max_length=100,
                                blank=False,
                                 default='2')
    def __str__(self):
        return self.name


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to='static/item_images', blank=False)
    image2 = models.ImageField(upload_to='static/item_images', blank=True)
    image3 = models.ImageField(upload_to='static/item_images', blank=True)
    image4 = models.ImageField(upload_to='static/item_images', blank=True)
    image5 = models.ImageField(upload_to='static/item_images', blank=True)


class ItemComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField()
    comment = models.TextField(blank=False)



class OfferComment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=250)

class ItemOffer(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE,related_name="primary_item")
    offer_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="offer_item")
    is_current = models.BooleanField(default=True)
    current_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="current_item_bidder")
    original_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="original_item_bidder")

class CashOffer(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    offer_amount = models.DecimalField(max_digits=9,
                                       decimal_places=2,
                                       blank=False)
    is_current = models.BooleanField(default=True)
    current_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="current_cash_bidder")
    original_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="original_cash_bidder")




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class Offer(models.Model):
    bid_on = models.ForeignKey(Item, related_name='item_bid_on', on_delete=models.CASCADE)
    bid_with = models.ForeignKey(Item, related_name='item_bid_with', on_delete=models.CASCADE)
