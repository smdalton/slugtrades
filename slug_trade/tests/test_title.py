import bengal

def test_title(browser):
    elem = browser.title
    bengal.check_equal(elem, "Home")

bengal.run_test(test_title)
