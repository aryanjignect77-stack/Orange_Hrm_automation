import random
from selenium.webdriver.common.by import By
from data_objects.edit_job_details.edit_job_details import EditJobDetails
from page_objects.base.base_page import BasePage

class EmployeeListPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    save_button = (By.XPATH,"//button[@type='submit']")

    def get_text_box_by_label(self, label_name):
        return (By.XPATH,f"//label[text()='{label_name}']/ancestor::div[contains(@class,'oxd-input-group')]//input")

    def get_dropdown_by_label(self, label_name):
        return (By.XPATH,f"//label[text()='{label_name}']/ancestor::div[contains(@class,'oxd-input-group')]//div[contains(@class,'oxd-select-text-input')]")

    def get_tab_by_name(self, tab_name):
        return (By.XPATH,f"//div[@class='orangehrm-tabs-wrapper']//a[normalize-space()='{tab_name}']")

    def get_date_input_by_label(self):
        return (
            By.XPATH,
            f"//label[normalize-space()='Joined Date']"
            f"/ancestor::div[contains(@class,'oxd-input-group')]"
            f"//input"
        )

    def get_dropdown_by_label(self, label_name):
        return (By.XPATH,f"//label[normalize-space()='{label_name}'] "
                         f"/ancestor::div[contains(@class,'oxd-input-group')]"
                         f"//div[contains(@class,'oxd-select-text--active')]")

    def get_all_dropdown_options(self):
        return (
            By.XPATH,
            '//div[@class="oxd-select-option"]//span'
        )

    def get_sub_unit_options(self):
        return (By.XPATH,"//div[@role='listbox']//div[@role='option'][not(normalize-space()='-- Select --')]")

    def get_selected_dropdown_value_by_label(self, label_name):
        return self.selenium.get_text(
            (
                By.XPATH,
                f"//label[normalize-space()='{label_name}']"
                f"/ancestor::div[contains(@class,'oxd-input-group')]"
                f"//div[contains(@class,'oxd-select-text--active')]"
                f"//div[contains(@class,'oxd-select-text-input')"
                f" and normalize-space()!='-- Select --']"
            )
        )

    def get_date_value_by_label(self, label_name):
        return self.selenium.get_attribute(
            (
                By.XPATH,
                f"//label[normalize-space()='{label_name}']"
                f"/ancestor::div[contains(@class,'oxd-input-group')]"
                f"//input"
            ),
            "value"
        )

    def update_job_details_and_click_on_save_button(self,edit_job_details: EditJobDetails) -> EditJobDetails:
        self.selenium.clear_and_type(
            self.get_date_input_by_label(),
            edit_job_details.joined_date
        )

        self.selenium.wait_till_clickable(self.get_dropdown_by_label("Job Title")).click()
        job_title = self.selenium.wait_for_elements(self.get_all_dropdown_options())
        selected_job_title = random.choice(job_title)
        edit_job_details.job_title = selected_job_title.text
        selected_job_title.click()

        self.selenium.wait_till_clickable(self.get_dropdown_by_label("Job Category")).click()
        job_category = self.selenium.wait_for_elements(self.get_all_dropdown_options())
        selected_job_category = random.choice(job_category)
        edit_job_details.job_category = selected_job_category.text
        selected_job_category.click()

        self.selenium.wait_till_clickable(self.get_dropdown_by_label("Sub Unit")).click()
        sub_unit = self.selenium.wait_for_elements(self.get_sub_unit_options())
        selected_sub_unit = random.choice(sub_unit)
        edit_job_details.sub_unit = selected_sub_unit.text
        selected_sub_unit.click()

        self.selenium.wait_till_clickable(self.get_dropdown_by_label("Location")).click()
        job_location = self.selenium.wait_for_elements(self.get_all_dropdown_options())
        selected_job_location = random.choice(job_location)
        edit_job_details.location = selected_job_location.text
        selected_job_location.click()

        self.selenium.wait_till_clickable(self.get_dropdown_by_label("Employment Status")).click()
        employment_status = self.selenium.wait_for_elements(self.get_all_dropdown_options())
        selected_employment_status = random.choice(employment_status)
        edit_job_details.employment_status = selected_employment_status.text
        selected_employment_status.click()

        self.selenium.wait_till_clickable(self.save_button).click()

    def enter_text_in_text_box_by_label(self, label_name, text):
        self.selenium.clear_and_type(self.get_text_box_by_label(label_name),text)

    def click_on_tab_by_name(self, tab_name):
        self.selenium.wait_till_clickable(self.get_tab_by_name(tab_name)).click()
        self.wait_for_loader_to_disappear()




