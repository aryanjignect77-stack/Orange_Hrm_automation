from selenium.webdriver.common.by import By
from page_objects.base.base_page import BasePage

class PimPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    employee_list = (By.XPATH,"//a[normalize-space()='Employee List']")
    personal_details_text = (By.XPATH,"//h6[normalize-space()='Personal Details']")

    edit_icon_button = (By.XPATH,f"//button[@class='oxd-icon-button oxd-table-cell-action-space']"
                                 f"//i[@class='oxd-icon bi-pencil-fill']")

    def get_input_field_by_label(self, label_name):
        return (By.XPATH,f"//label[normalize-space()='{label_name}']"
                f"/ancestor::div[contains(@class,'oxd-input-group')]"
                f"//input")

    def get_button_by_name(self, button_name):
        return (By.XPATH,f"//button[normalize-space()='{button_name}']")

    def get_header_text_by_name(self, page_name):
        return (By.XPATH,f"//h5[normalize-space()='{page_name}']")

    def get_employee_id_from_search_result(self, employee_id):
        locator = (
            By.XPATH,f"//div[@class='oxd-table-cell oxd-padding-cell'][normalize-space()='{employee_id}']"
        )
        return self.selenium.get_text(locator).strip()

    def get_employee_name_from_search_result(self, employee_name):
        locator = (By.XPATH,f"//div[@class='oxd-table-cell oxd-padding-cell'][normalize-space()='{employee_name}']")
        return self.selenium.get_text(locator).strip()

    def get_tab_by_name(self, tab_name):
        return (By.XPATH,f"//a[contains(@class,'orangehrm-tabs-item') and normalize-space()='{tab_name}']")

    def click_on_edit_icon_button(self):
        self.selenium.wait_till_clickable(
            (By.XPATH, f"//button[@class='oxd-icon-button oxd-table-cell-action-space']"
                       f"//i[@class='oxd-icon bi-pencil-fill']")
        ).click()

    def is_personal_details_text_visible(self):
        self.wait_for_loader_to_disappear()
        return self.selenium.wait_till_visible(self.personal_details_text)

    def click_on_employee_list_link(self):
        self.selenium.wait_till_clickable(self.employee_list).click()

    def is_header_text_visible(self, header_text):
        return self.selenium.wait_till_visible(self.get_header_text_by_name(header_text))

    def click_on_button_by_name(self, button_name):
        self.selenium.wait_till_clickable(self.get_button_by_name(button_name)).click()

    def click_on_tab_by_name(self, tab_name):
        self.selenium.wait_till_clickable(self.get_tab_by_name(tab_name)).click()

    def search_employee_by_name(self, label_name,employee_name):
        self.selenium.clear_and_type(self.get_input_field_by_label(label_name), employee_name)




