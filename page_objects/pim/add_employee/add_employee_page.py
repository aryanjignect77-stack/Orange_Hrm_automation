from selenium.webdriver.common.by import By
from page_objects.base.base_page import BasePage

class AddEmployeePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    add_employee_text = (By.CSS_SELECTOR,"h6.oxd-text.oxd-text--h6.orangehrm-main-title")
    create_login_details_toggle_button = (By.XPATH,"//div[@class='oxd-switch-wrapper']")
    save_button = (By.XPATH,"//button[normalize-space()='Save']")

    # success_toast_message = (By.CSS_SELECTOR,"div.oxd-toast.oxd-toast--success.oxd-toast-container--toast")

    # def is_success_toast_displayed(self):
    #     return self.selenium.wait_till_visible(self.success_toast_message)

    def is_add_employee_text_displayed(self):
        return self.selenium.wait_till_visible(self.add_employee_text)

    def get_input_field_by_name(self, field_name):
        return (By.NAME, field_name)

    def get_input_by_label(self, label_text):
        return (
            By.XPATH,
            f"//label[normalize-space()='{label_text}']/ancestor::div[contains(@class,'oxd-input-group')]//input"
        )

    def click_on_save_button(self):
        self.selenium.wait_till_clickable(self.save_button).click()

    def add_employee_details_and_save(self, employee):
        self.selenium.clear_and_type(self.get_input_field_by_name("firstName"), employee.first_name)
        self.selenium.clear_and_type(self.get_input_field_by_name("middleName"), employee.middle_name)
        self.selenium.clear_and_type(self.get_input_field_by_name("lastName"), employee.last_name)
        self.selenium.clear_and_type(self.get_input_by_label("Employee Id"), employee.employee_id)

        self.click_on_create_login_details_toggle_button()
        # self.wait_for_loader_to_disappear()

        self.selenium.clear_and_type(self.get_input_by_label("Username"), employee.username)
        self.selenium.clear_and_type(self.get_input_by_label("Password"), employee.password)
        self.selenium.clear_and_type(self.get_input_by_label("Confirm Password"), employee.confirm_password)
        self.click_on_save_button()

    def fill_name_and_details(self, employee):
        self.selenium.clear_and_type(self.get_input_field_by_name("firstName"), employee.first_name)
        self.selenium.clear_and_type(self.get_input_field_by_name("middleName"), employee.middle_name)
        self.selenium.clear_and_type(self.get_input_field_by_name("lastName"), employee.last_name)
        self.selenium.clear_and_type(self.get_input_by_label("Employee Id"), employee.employee_id)

    def fill_login_details(self, employee):
        self.selenium.clear_and_type(self.get_input_by_label("Username"), employee.username)
        self.selenium.clear_and_type(self.get_input_by_label("Password"), employee.password)
        self.selenium.clear_and_type(self.get_input_by_label("Confirm Password"), employee.confirm_password)

    def click_on_create_login_details_toggle_button(self):
        self.wait_for_loader_to_disappear()
        self.selenium.wait_till_clickable(self.create_login_details_toggle_button).click()







