from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User
from .. import models as slug_models
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.core.files import File
from django.utils.six import BytesIO
from PIL import Image
from io import StringIO

def create_image(filename, storage=None, size=(100,100), image_mode='RGB', image_format='PNG'):
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)

"""
#Pre
"""
#Post
class CashTransactionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        bid_receiver = User(name='BidReceiver', lastname='BidReceiver').save()
        bid_placer = User(name='BidPlacer', lastname='BidPlacer').save()
        item_bid_on = slug_models.Item(
            user=bid_receiver,
            name='ItemBidOnWithCash',
            price=10.12,
            category='O',
            trade_options='0',

        ).save()
        fail_trade_item_bid_on =slug_models.Item(
            user=bid_receiver,
            name='ItemBidOnWithCash',
            price=10.12,
            category='O',
            trade_options='1',
        ).save()
        fail_free_item_bid_on =slug_models.Item(
            user=bid_receiver,
            name='ItemBidOnWithCash',
            price=10.12,
            category='O',
            trade_options='2',

        ).save()

        for item in [item_bid_on, fail_free_item_bid_on, fail_trade_item_bid_on]:
            item_image = slug_models.ItemImage(
                user=bid_receiver,
                item=item,
                image1=create_image(item.name)
            ).save()



    def test_details(self):
        #ensure that only the cash transaction has succeeded

        # use trade_item

        # use free_item

        # user cash_item
        cash_offer = slug_models.CashOffer()







# class ItemTransactionTestCase(TestCase):
#
# class MultipleItemTransactionTestCase(TestCase):