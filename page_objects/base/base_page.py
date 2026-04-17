from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from utilities.selenium_helpers import SeleniumHelpers

class BasePage:
    """
    BasePage class.
    All Page Object classes should extend this class.
    """

    def __init__(self, driver):
        self.driver = driver
        self.selenium = SeleniumHelpers(driver)

    form_loader = (By.CSS_SELECTOR, ".oxd-form-loader")

    def wait_for_loader_to_disappear(self, timeout=25):
        try:
            self.selenium.wait_till_invisible(self.form_loader, timeout)
        except TimeoutException:
            pass