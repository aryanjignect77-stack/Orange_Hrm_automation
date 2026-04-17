import random
from selenium.webdriver.common.by import By
from page_objects.pim.qualifications.qualifications_page import QualificationsPage

class RecruitmentPage(QualificationsPage):

    def __init__(self, driver):
        super().__init__(driver)

    notes_text_area = (By.XPATH,"//textarea[@class='oxd-textarea oxd-textarea--active oxd-textarea--resize-vertical']")
    edit_radio_button = (By.XPATH,"//span[contains(@class,'oxd-switch-input') and contains(@class,'--label-left')]")

    def get_input_field_by_name_(self, field_name):
        return (By.XPATH,f"//input[@placeholder='{field_name}']")

    def get_candidate_name_cell_locator(self, candidate_name):
        return (
            By.XPATH,
            f"//div[@role='row']"
            f"//div[@role='cell']//div[normalize-space()='{candidate_name}']"
        )

    def select_candidate_from_autocomplete(self, candidate_name):
        locator = (
            By.XPATH,
            f"//div[@role='listbox']//span[normalize-space()='{candidate_name}']"
        )
        self.selenium.wait_till_visible(locator)
        self.selenium.click(locator)

    def get_action_button_by_candidate_and_action(self, candidate_name, action):
        action_icon_map = {
            "view": "bi-eye-fill",
            "delete": "bi-trash",
            "download": "bi-download"
        }
        icon_class = action_icon_map[action.lower()]
        return (
            By.XPATH,
            f"//div[@role='row']"
            f"[.//div[normalize-space()='{candidate_name}']]"
            f"//button[.//i[contains(@class,'{icon_class}')]]"
        )

    def is_confirmation_pop_up_displayed(self):
        locator = (By.XPATH,"//p[@class='oxd-text oxd-text--p oxd-text--card-title']")
        return self.selenium.wait_till_visible(locator)

    def get_input_field_value_by_name(self, field_name):
        locator = self.get_input_field_by_name_(field_name)
        return self.selenium.get_attribute(locator, "value")

    def click_action_button_for_candidate(self, candidate_name, action):
        locator = self.get_action_button_by_candidate_and_action(candidate_name, action)
        self.selenium.click(locator)

    def fill_candidate_details(self, recruitment):
        self.selenium.clear_and_type(self. get_input_field_by_name_("First Name"),recruitment.first_name)
        self.selenium.clear_and_type(self.get_input_field_by_name_("Middle Name"),recruitment.middle_name)
        self.selenium.clear_and_type(self.get_input_field_by_name_("Last Name"),recruitment.last_name)

        self.click_on_dropdown_label_by_name("Vacancy")
        vacancy_options = self.selenium.wait_for_elements(self.get_all_dropdown_options())
        selected_vacancy = random.choice(vacancy_options)
        recruitment.vacancy = selected_vacancy.text
        selected_vacancy.click()

        self.selenium.clear_and_type(self.get_input_field_by_name("Email"),recruitment.email)
        self.selenium.clear_and_type(self.get_input_field_by_name("Contact Number"),recruitment.contact_number)
        self.selenium.clear_and_type(self.get_input_field_by_name("Keywords"),recruitment.keywords)
        self.selenium.clear_and_type(self.get_input_field_by_name("Date of Application"),recruitment.date_of_application)
        self.selenium.clear_and_type(self.notes_text_area,recruitment.notes)
        self.click_on_save_button()

    def search_candidate_by_name(self, recruitment):
        self.selenium.clear_and_type(self.get_input_field_by_name("Candidate Name"),recruitment.name)

    def click_edit_radio_button(self):
        self.selenium.wait_till_clickable(self.edit_radio_button).click()

    def get_displayed_candidate_name(self, candidate_name):
        locator = self.get_candidate_name_cell_locator(candidate_name)
        return self.selenium.get_text(locator)

    def update_candidate_details(self, recruitment):
        self.selenium.clear_and_type(self.get_input_field_by_name_("First Name"), recruitment.first_name)
        self.selenium.clear_and_type(self.get_input_field_by_name_("Middle Name"), recruitment.middle_name)
        self.selenium.clear_and_type(self.get_input_field_by_name_("Last Name"), recruitment.last_name)

        self.click_on_dropdown_label_by_name("Job Vacancy")
        vacancy_options = self.selenium.wait_for_elements(self.get_all_dropdown_options())
        selected_vacancy = random.choice(vacancy_options)
        recruitment.vacancy = selected_vacancy.text
        selected_vacancy.click()

        self.selenium.clear_and_type(self.get_input_field_by_name("Email"), recruitment.email)
        self.selenium.clear_and_type(self.get_input_field_by_name("Contact Number"), recruitment.contact_number)
        self.selenium.clear_and_type(self.get_input_field_by_name("Keywords"), recruitment.keywords)
        self.selenium.clear_and_type(self.get_input_field_by_name("Date of Application"),
                                     recruitment.date_of_application)
        self.selenium.clear_and_type(self.notes_text_area, recruitment.notes)
        self.click_on_save_button()





