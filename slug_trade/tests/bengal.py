from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
import platform

def check_exists(expected):
    if not expected:
        raise AssertionError("expected " + str(expected) + ", got null")

def check_equal(got, expected):
    if got != expected:
        raise AssertionError("expected " + str(expected) + ", got " + str(got))

def find_element_by_id(browser, elem_id):
    try:
        return browser.find_element_by_id(elem_id)
    except NoSuchElementException:
        raise AssertionError("expected element " + elem_id + " not found")


"""Drives each test."""
def run_test(func):
    dirname = os.path.dirname(__file__)

    if platform.system() == 'Darwin':
        path = dirname + '/drivers/mac/chromedriver'
    elif platform.system() == 'Linux':
        path = dirname + '/drivers/linux/chromedriver'

    browser = webdriver.Chrome(path)
    browser.get('localhost:8000')

    try:
        func(browser)
        print(func.__name__ +  ": PASS")
    except AssertionError as err:
        print(str(err))
        print(func.__name__ +  ": FAIL")

    browser.close()
