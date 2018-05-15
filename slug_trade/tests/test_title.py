import bengal

def test_title(browser):
    bengal.find_element_by_class_name(browser, "nav-logo")

bengal.run_test(test_title)
