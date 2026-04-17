from selenium.webdriver.common.by import By
from page_objects.base.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    login_button = (By.CSS_SELECTOR,"button.oxd-button.oxd-button--medium.oxd-button--main.orangehrm-login-button[type='submit']")
    invalid_credentials = (By.XPATH,"//p[normalize-space()='Invalid credentials']")

    def get_header_text_by_name(self, text_name):
        return (By.XPATH,f"//h5[@class='oxd-text oxd-text--h5 orangehrm-login-title'][text()='{text_name}']")

    def text_box_field_by_name(self, field_name):
        return (By.CSS_SELECTOR, f"input.oxd-input[name='{field_name}']")

    def click_on_login_button(self):
        self.selenium.wait_till_clickable(self.login_button)
        self.selenium.click(self.login_button)

    def enter_login_details(self,username,password):
        self.selenium.clear_and_type(self.text_box_field_by_name("username"),username)
        self.selenium.clear_and_type(self.text_box_field_by_name("password"),password)
        self.click_on_login_button()

    def is_invalid_credentials_text_displayed(self):
        return self.selenium.wait_till_visible(self.invalid_credentials)