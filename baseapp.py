from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, by, selector, timeout=10):
        locator = (by, selector)
        res = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator),
            message=f"Can't find element by locator {locator}"
        )
        return res

    def find_elements(self, by, selector, timeout=10):
        locator = (by, selector)
        res = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator),
            message=f"Can't find elements by locator {locator}"
        )
        return res
