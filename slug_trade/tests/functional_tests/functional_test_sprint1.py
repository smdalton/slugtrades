from selenium import webdriver
import unittest

#each functional test is based on the documentation of a user story
class BasicFunctionalityTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # wipe db
        # makemigrations
        # start runserver on port
        self.browser_address = 'http://localhost:8005'

    def tearDown(self):
        self.browser.quit()


    # As a user, I want a basic landing page so that I can navigate the site.
    def test_can_visit_home_page(self):
        """
            Show a landing page with links to:
            ■ Profile
            ■ Edit Profile
            ■ Products
            ■ LogIn
            ■ Log Out
            ■ Sign Up
        """
        self.browser.get(self.browser_address)
        self.assertIn('Home', self.browser.title)



    # As a user, I want to sign up.
    def test_can_create_account(self):
        """
            ■ First Name
            ■ Last Name
            ■ Email Address
            ■ Password
            ■ Verification Password
            ■ Profile Picture
        """
        pass

    # as a user I want to view my profile
    def test_can_view_profile(self):
        pass

    def test_can_edit_account(self):
        pass

    def test_can_view_item(self):
        pass

    def test_can_post_item(self):
        pass

    def test_cam_edit_item(self):
        pass
