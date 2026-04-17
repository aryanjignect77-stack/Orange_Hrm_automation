from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from typing import Callable, Any

class WaitHelpers:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_till_visible(self, locator, timeout=25):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_till_clickable(self, locator, timeout=30):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_till_element_is_clickable(self, element, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(element)
        )
        return element

    def wait_until_form_loaded(self, locator, timeout=15):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.find_element(*locator).get_attribute("value") != ""
        )

    def wait_till_present(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def wait_till_invisible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )

    def wait_until_condition(
            self,
            condition_fn: Callable[..., Any],
            *args,
            timeout: int = 10
    ):
        """
        Wait until condition_fn(*args) returns truthy.
        """
        return WebDriverWait(self.driver, timeout).until(
            lambda _: condition_fn(*args)
        )

    def wait_for_elements(self, locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )
        return self.driver.find_elements(*locator)

    def wait_for_elements_(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_all_elements_located(locator)
        )

