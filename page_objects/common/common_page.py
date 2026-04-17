from selenium.webdriver.common.by import By
from page_objects.base.base_page import BasePage

class CommonPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    success_toast_message = (By.CSS_SELECTOR,"div.oxd-toast.oxd-toast--success.oxd-toast-container--toast")

    def is_success_toast_message_displayed(self) -> bool:
        return self.selenium.wait_till_visible(self.success_toast_message)

    def get_form_header_text(self, form_name):
        return (By.XPATH,f"//h6[normalize-space()='{form_name}']")

    def is_form_displayed(self, form_name):
        return self.selenium.is_element_displayed(self.get_form_header_text(form_name))

    def is_form_header_text_displayed(self, form_name):
        locator = (By.XPATH,f"//h5[@class='oxd-text oxd-text--h5 oxd-table-filter-title'][normalize-space()='{form_name}']")
        return self.selenium.is_element_displayed(locator)