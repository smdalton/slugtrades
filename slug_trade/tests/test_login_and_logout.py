import time
from selenium.webdriver import ActionChains
import bengal

def test_login_and_logout(browser):
    elem = bengal.find_element_by_id(browser, "login")
    elem.click()
    elem = bengal.find_element_by_id(browser, "id_username")
    elem.send_keys("admin")
    elem = bengal.find_element_by_id(browser, "id_password")
    elem.send_keys("pass1234")
    elem = bengal.find_element_by_id(browser, "login_submit")
    elem.click()

    nav_links = bengal.find_element_by_id(browser, "links_drop")
    logout = bengal.find_element_by_id(browser, "logout")
    actions = ActionChains(browser)
    actions.move_to_element(nav_links)
    actions.click(logout)
    actions.perform()

    elem = bengal.find_element_by_id(browser, "login")

bengal.run_test(test_login_and_logout)
