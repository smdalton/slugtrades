from time import sleep

from selenium import webdriver
import unittest

#each functional test is based on the documentation of a user story

class BasicFunctionalityTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    # As a user, I want a basic landing page so that I can navigate the site.
    # def test_can_visit_home_page_and_sign_up(self):
    #     """
    #         Show a landing page with links to:
    #         ■ Profile
    #         ■ Edit Profile
    #         Products
    #         LogIn
    #         ■ Log Out
    #         ■ Sign Up
    #     """
    #     self.browser.get('http://localhost:8001')
    #     self.assertIn('Home', self.browser.title)
    #     navigation_buttons = self.browser.find_elements_by_class_name("nav-link-button")
    #     self.assertIn('Products', [btn.text for btn in navigation_buttons])
    #     self.assertIn('How It Works', [btn.text for btn in navigation_buttons])
    #     self.assertIn('Login', [btn.text for btn in navigation_buttons])
    #     self.assertIn('Sign Up', [btn.text for btn in navigation_buttons])

    def test_can_sign_up(self):
        """
            ■ First Name
            ■ Last Name
            ■ Email Address
            ■ Password
            ■ Verification Password
            ■ Profile Picture
        """
        # go to signup route via button
        self.browser.get('http://localhost:8001')
        self.browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/button[2]').click()
        fname = self.browser.find_element_by_id('first-name')
        lname = self.browser.find_element_by_id('last-name')
        email = self.browser.find_element_by_id('id_email')
        passwd1 = self.browser.find_element_by_id('id_passwd1')
        passwd2 = self.browser.find_element_by_id('id_passwd2')
        # click on signup button





    # def test_can_login(self):
    #     pass
    #
    # def test_can_logout(self):
    #     pass


if __name__ == '__main':
    print('opening test1')
    unittest.main()
else:
    unittest.main()