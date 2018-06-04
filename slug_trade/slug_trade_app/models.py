from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from datetime import datetime
from django.utils import timezone


ITEM_CATEGORIES = (
    ('E', 'Electronics'),
    ('H', 'Household'),
    ('C', 'Clothing'),
    ('O', 'Other'),
    ('BI', 'Bikes'),
    ('BO', 'Books'),
    ('MO', 'Movies'),
    ('MU', 'Music'),
    ('I', 'Instruments'),
    ('TI', 'Tickets'),
    ('TO', 'Tools'),
    ('TOY', 'Toys'),
    ('G', 'Gaming'),
    ('OU', 'Outdoors'),
    ('OF', 'Office'),
    ('F', 'Furniture'),
    ('A', 'Appliances'),
    ('FI', 'Fitness')
)

CAMPUS_STATUS = (
    ('on', 'Located on campus'),
    ('off', 'Located off campus')
)

TRADE_OPTIONS = (
    ('0','Cash Only'),
    ('1','Items Only'),
    ('2','Free')
)


ITEM_CONDITION = (
    ('0','Well Loved'),
    ('1','Fair'),
    ('2','Good'),
    ('3','Like New'),
    ('4','New')
)

#class User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='static/profile_pictures', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    time_stamp = models.DateTimeField(auto_now=True, null=True)
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
    category = models.CharField(max_length=8,
                                default="O",
                                choices=ITEM_CATEGORIES,
                                blank=False)
    trade_options = models.CharField(max_length=80,
                                     default='1',
                                    choices=TRADE_OPTIONS,
                                    blank=False)
    bid_counter = models.IntegerField(default=0, blank=False)
    description = models.TextField(blank=False, default='')
    # time_stamp = models.DateTimeField(auto_now=True, null=True)
    time_stamp = models.DateTimeField(default=datetime.now(), null=True)
    condition = models.CharField(choices=ITEM_CONDITION,
                                max_length=100,
                                blank=False,
                                 default='2')
    def get_images(self):
        try:
            a = ItemImage.objects.get(item__id=self.id).get_image_list()
            return a[0]
        except Exception:
            return 'error retrieving image'

    def __str__(self):
        return self.name


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to='static/item_images', blank=False)
    image2 = models.ImageField(upload_to='static/item_images', blank=True)
    image3 = models.ImageField(upload_to='static/item_images', blank=True)
    image4 = models.ImageField(upload_to='static/item_images', blank=True)
    image5 = models.ImageField(upload_to='static/item_images', blank=True)

    def get_image_list(self):
        result = []
        if self.image1:
            result.append(self.image1.url)
        if self.image2:
            result.append(self.image2.url)
        if self.image3:
            result.append(self.image3.url)
        if self.image4:
            result.append(self.image4.url)
        if self.image5:
            result.append(self.image5.url)
        return result

    def __str__(self):
        return f"{self.item}"


class ItemComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now=True)
    comment = models.TextField(blank=False)


class OfferComment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offer_comments")
    comment_placed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.comment[:20]}"


class ItemOffer(models.Model):
    item_bid_on = models.ForeignKey(Item, on_delete=models.CASCADE,related_name="item_offers_item_bid_on")
    item_bid_with = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item_offers_bid_with")
    time_stamp = models.DateTimeField(auto_now=True, null=True)
    item_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    original_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="item_offers_original_bidder")

    def get_images(self):
        try:
            a = ItemImage.objects.get(item__id=self.item_bid_with.id).get_image_list()
            return a[0]
        except Exception:
            return 'error retrieving image'

    def __str__(self):
        return f" Bid on: {self.item_bid_on.name} With: {self.item_bid_with}"

class CashOffer(models.Model):
    item_bid_on = models.ForeignKey(Item, on_delete=models.CASCADE)
    offer_amount = models.DecimalField(max_digits=9,
                                       decimal_places=2,
                                       blank=False)
    time_stamp = models.DateTimeField(auto_now=True, null=True)
    item_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cash_offers_item_owner")
    original_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cash_offers_original_bidder")


class Offer(models.Model):
    bid_on = models.ForeignKey(Item, related_name='item_bid_on', on_delete=models.CASCADE)
    bid_with = models.ForeignKey(Item, related_name='item_bid_with', on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now=True, null=True)
