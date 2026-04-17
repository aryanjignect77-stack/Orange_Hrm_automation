import random

from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from utilities.wait_helpers import WaitHelpers


class SeleniumHelpers(WaitHelpers):
    """
    Selenium interaction helpers.
    All element actions should go through this class.
    """

    def __init__(self, driver):
        super().__init__(driver)

    def get_text(self, locator):
        element = self.wait_till_visible(locator)
        return element.text.strip()


    def find_element(self, locator):
        return self.wait_till_visible(locator)

    def click(self, locator):
        element = self.wait_till_clickable(locator)
        element.click()
        return self

    def clear_and_type(self, locator, value):
        element = self.wait_till_visible(locator)
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(value)

    def overlay_click(self, locator):
        try:
            element = self.wait_till_clickable(locator)
            element.click()
        except Exception:
            self.javascript_click(locator)

    def wait_till_present(driver, locator, timeout=5):
        try:
            WebDriverWait(
                driver,
                timeout,
                poll_frequency=0.2,
                ignored_exceptions=(StaleElementReferenceException,)
            ).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def wait_till_present_(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def enter_text(self, locator, text):
        element = self.wait_till_visible(locator)
        element.clear()
        element.send_keys(text)

    def type(self, locator, value, timeout: int = 10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(value)

    def fill_input(self, locator, value, timeout: int = 10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        element.clear()
        element.send_keys(value)

    # ---------------- GETTERS ---------------- #

    def get_text(self, locator):
        return self.wait_till_visible(locator).text

    def get_attribute(self, locator, attribute):
        return self.wait_till_visible(locator).get_attribute(attribute)

    def is_element_displayed(self, locator) -> bool:
        try:
            element = self.wait_till_visible(locator)
            return element.is_displayed()
        except TimeoutException:
            return False

    def upload_file(self, locator, file_path):
        element = self.wait_till_present_(locator)
        element.send_keys(file_path)

    # ---------------- DROPDOWN ---------------- #

    def select_by_visible_text(self, locator, text):
        element = self.wait_till_visible(locator)
        Select(element).select_by_visible_text(text)

    def select_by_value(self, locator, value):
        element = self.wait_till_visible(locator)
        Select(element).select_by_value(value)

    # ---------------- ACTION CHAINS ---------------- #

    def hover_over_element(self, locator):
        element = self.wait_till_visible(locator)
        ActionChains(self.driver).move_to_element(element).perform()

    # ---------------- JAVASCRIPT ---------------- #

    def javascript_click(self, locator):
        element = self.wait_till_present(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def scroll_into_view(self, locator):
        element = self.wait_till_present(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    # ---------------- PAGE UTILITIES ---------------- #

    def get_page_title(self):
        return self.driver.title

    def get_current_url(self):
        return self.driver.current_url

    def refresh_page(self):
        self.driver.refresh()

    # ---------------- SCREENSHOT ---------------- #

    def take_screenshot(self, filename):
        self.driver.save_screenshot(filename)

    def get_elements(self, locator):
        return self.driver.find_elements(*locator)

    def select_random_option_from_elements(self, selected_element, option_elements):
        """
        selected_element  -> WebElement showing current value
        option_elements   -> list[WebElement] of dropdown options
        """

        current_value = selected_element.text.strip()

        valid_options = [
            opt for opt in option_elements
            if opt.is_displayed() and opt.text.strip() != current_value
        ]

        random.choice(valid_options).click()

    def wait_till_attribute_changes(self, locator, attribute_name, old_value, timeout=15):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.find_element(*locator)
            .get_attribute(attribute_name) != old_value
        )