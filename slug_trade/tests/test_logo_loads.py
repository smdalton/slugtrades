import bengal

def test_logo_loads(browser):
    bengal.find_element_by_class_name(browser, "nav-logo")

bengal.run_test(test_logo_loads)
