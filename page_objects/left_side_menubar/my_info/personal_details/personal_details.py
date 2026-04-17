from selenium.webdriver.common.by import By
from page_objects.base.base_page import BasePage

class PersonalDetails(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def get_input_field_by_name(self, field_name):
        return (By.XPATH,f"//input[@name='{field_name}']")

    save_button = (By.XPATH,"//div[@class='orangehrm-horizontal-padding orangehrm-vertical-padding']//button[@type='submit'][normalize-space()='Save']")
    employee_image_icon = (By.CSS_SELECTOR,"div.orangehrm-edit-employee-image")
    add_image_button = (By.CSS_SELECTOR,"button.oxd-icon-button.oxd-icon-button--solid-main.employee-image-action")
    profile_picture_file_input = (By.XPATH, "//input[@type='file']")
    profile_dropdown_image = (
        By.XPATH,
        "//img[contains(@class,'oxd-userdropdown-img')]"
    )

    def get_form_title_by_name(self, form_name):
        return (By.XPATH,f"//h6[@class='oxd-text oxd-text--h6 orangehrm-main-title'][normalize-space()='{form_name}']")

    def get_dropdown_by_label(self, label_name):
        return (By.XPATH,f"//label[normalize-space()='{label_name}']"
                f"/ancestor::div[contains(@class,'oxd-input-group')]"
                f"//div[contains(@class,'oxd-select-text-input')]"
        )

    def get_selected_dropdown_value_element(self, label_name):
        return self.driver.find_element(
            By.XPATH,
            f"//label[normalize-space()='{label_name}']"
            f"/ancestor::div[contains(@class,'oxd-input-group')]"
            f"//div[contains(@class,'oxd-select-text-input')]"
        )

    def get_dropdown_options(self):
        return self.driver.find_elements(
            By.XPATH,
            "//div[@role='option']//span"
        )

    def enter_text_in_field(self, edit_info):
        self.selenium.wait_till_visible(self.get_input_field_by_name("firstName"))
        self.selenium.clear_and_type(self.get_input_field_by_name("firstName"),edit_info.first_name)
        self.selenium.clear_and_type(self.get_input_field_by_name("middleName"),edit_info.middle_name)
        self.selenium.clear_and_type(self.get_input_field_by_name("lastName"),edit_info.last_name)
        self.selenium.clear_and_type(self.get_input_by_label("Other Id"),edit_info.other_id)

    def get_updated_personal_details(self):
        return {
        "firstName":self.selenium.get_attribute(self.get_input_field_by_name("firstName"),"value"),
        "middleName":self.selenium.get_attribute(self.get_input_field_by_name("middleName"),"value"),
        "lastName":self.selenium.get_attribute(self.get_input_field_by_name("lastName"),"value"),
        "Other Id":self.selenium.get_attribute(self.get_input_by_label("Other Id"),"value"),
        }

    def get_input_by_label(self, label):
        return (
            By.XPATH,
            f"//label[normalize-space()='{label}']"
            f"/ancestor::div[contains(@class,'oxd-input-group')]//input"
        )

    def upload_image(self, image_path):
        self.selenium.upload_file(self.profile_picture_file_input, image_path)
        self.selenium.wait_till_clickable(self.save_button).click()

    def click_on_profile_picture(self):
        self.selenium.wait_till_clickable(self.employee_image_icon).click()

    def click_on_save_button(self):
        self.selenium.click(self.save_button)

    def click_on_dropdown(self, label_name):
        self.selenium.click(self.get_dropdown_by_label(label_name))

    def select_random_dropdown_value(self, label_name):
        self.click_on_dropdown(label_name)
        selected_element = self.get_selected_dropdown_value_element(label_name)
        option_elements = self.get_dropdown_options()
        self.selenium.select_random_option_from_elements(
            selected_element,
            option_elements
        )