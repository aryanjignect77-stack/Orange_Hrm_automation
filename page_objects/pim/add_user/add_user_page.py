from selenium.webdriver.common.by import By
from page_objects.base.base_page import BasePage

class AddUserPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    employee_name_input = (By.XPATH,"//label[normalize-space()='Employee Name']/ancestor::div[contains(@class,'oxd-input-group')]//input")

    def get_form_text_by_name(self, form_name):
        return (By.XPATH,f"//h6[@class='oxd-text oxd-text--h6 orangehrm-main-title'][normalize-space()='{form_name}']")

    def get_dropdown_by_name(self, field_name):
        return (By.XPATH,f"//label[normalize-space()='{field_name}']"
                f"/ancestor::div[contains(@class,'oxd-input-group')]"
                f"//div[contains(@class,'oxd-select-text-input')]"
        )

    def get_input_field_by_name(self, field_name):
        return (By.XPATH,f"//label[normalize-space()='{field_name}']"
                f"/ancestor::div[contains(@class,'oxd-input-group')]"
                f"//input[contains(@class,'oxd-input')]"
        )

    def get_dropdown_option_by_text(self, option_text):
        return (By.XPATH, f"//div[@class='oxd-select-dropdown --positon-bottom']//span[normalize-space()='{option_text}']")

    def get_employee_name_suggestion(self, employee_name):
        return (By.XPATH,f"//div[@class='oxd-autocomplete-dropdown --positon-bottom']//div[normalize-space()='{employee_name}']")

    def user_fills_in_all_mandatory_fields_and_clicks_save(self, add_user_data):
        # User Role
        self.selenium.wait_till_clickable(self.get_dropdown_by_name("User Role")).click()
        self.selenium.wait_till_clickable(self.get_dropdown_option_by_text(add_user_data.user_role)).click()
        # Employee Name
        self.selenium.clear_and_type(self.employee_name_input,add_user_data.employee_name)
        self.selenium.wait_till_clickable(self.get_employee_name_suggestion(add_user_data.employee_name)).click()
        # Status
        self.selenium.wait_till_clickable(self.get_dropdown_by_name("Status")).click()
        self.selenium.wait_till_clickable(self.get_dropdown_option_by_text(add_user_data.status)).click()
        # Username & Passwords
        self.selenium.clear_and_type(self.get_input_field_by_name("Username"),add_user_data.username)
        self.selenium.clear_and_type(self.get_input_field_by_name("Password"),add_user_data.password)
        self.selenium.clear_and_type(self.get_input_field_by_name("Confirm Password"),add_user_data.password)
