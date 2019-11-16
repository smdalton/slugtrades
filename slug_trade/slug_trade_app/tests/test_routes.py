"""
Test that all routes return a correct http response

"""
import unittest
from django.test import Client
## Setup

# routes that are non-detail routes nor post submissions
# ensure that all routes that are meant to be authenticated are and vice-versa

simple_routes = [
    'home',
    'products',
    'login',
    'logout',
    'user_list_view',
    'signup',
    'item_details',
]

## required login
privileged_routes = [
    'profile',
    'edit_profile',
    'add_closet_item',
    'delete_from_wishlist',
    'my_received_offers',
    'my_placed_offers'
]

authentication_routes = ['login']


## test for get request to each route
class SimpleTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_details(self):
        responses = [(self.client.get('/' + url + '/').status_code, url) for url in simple_routes]
        for response in responses:

            self.assertEqual(response[0], (200 or 302))
            print("Status: " + response[1])


    # response = c.get('/customer/details/', {'name':'fred', 'age':7})
    # response.content
