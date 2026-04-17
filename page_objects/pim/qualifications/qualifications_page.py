import datetime
import random

from selenium.webdriver.common.by import By
from data_objects.qualifications.language.language import Language
from data_objects.qualifications.license.license import License
from page_objects.base.base_page import BasePage


class QualificationsPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    comment_text_area = (By.XPATH,"//textarea[contains(@class,'oxd-textarea')]")
    save_button = (By.XPATH, "//button[@type='submit']")
    attachment_input = (By.XPATH,"//input[@type='file' and contains(@class,'oxd-file-input')]")

    def get_add_button_by_form_name(self, form_name):
        return (By.XPATH,f"//h6[normalize-space()='{form_name}']/parent::div//button")

    def get_input_field_by_name(self, field_name):
        return (By.XPATH,f"//label[normalize-space()='{field_name}']/ancestor::div[contains(@class,'oxd-input-group')]//input")

    def get_header_by_name(self, header_name):
        return (
            By.XPATH,
            f"//div[@role='columnheader' and normalize-space()='{header_name}']"
        )

    def get_cell_by_company_and_header(self, company_name, header_name):
        return (
            By.XPATH,
            f"""
            //div[@role='row' and .//div[normalize-space()='{company_name}']]
            //div[@role='cell'][
                count(
                    preceding-sibling::div[@role='cell']
                ) =
                count(
                    //div[@role='columnheader' and normalize-space()='{header_name}']
                    /preceding-sibling::div[@role='columnheader']
                )
            ]
            """
        )

    def get_dropdown_label_by_name(self, label_name):
        return (By.XPATH,f"//label[normalize-space()='{label_name}']/ancestor::div[contains(@class,'oxd-input-group')]"
                f"//div[@class='oxd-select-text-input']")

    def get_random_dropdown_option_value(self, random_value):
        return (By.XPATH,f'//div[@class="oxd-select-option"]//span[normalize-space()="{random_value}"]')

    def get_all_dropdown_options(self):
        return (
            By.XPATH,
            '//div[@class="oxd-select-option"]//span'
        )

    def get_education_cell(self, level, col_index):
        return (
            By.XPATH,
            f'//h6[normalize-space()="Education"]'
            f'/following::div[@role="row" and .//div[normalize-space()="{level}"]]'
            f'//div[@role="cell"][{col_index}]//div'
        )

    def get_skill_cell_by_index(self, skill, col_index):
        return (
            By.XPATH,
            f'//div[@role="row" and contains(@class,"oxd-table-row")]'
            f'[.//div[normalize-space()="{skill}"]]'
            f'//div[@role="cell"][{col_index}]//div'
        )

    def get_language_cell_by_index(self, language, col_index):
        return (
            By.XPATH,
            f'//div[@role="row" and contains(@class,"oxd-table-row")]'
            f'[.//div[normalize-space()="{language}"]]'
            f'//div[@role="cell"][{col_index}]//div'
        )

    def get_license_cell_by_index(self, license, col_index):
        return (
            By.XPATH,f"//div[@role='row'][.//div[normalize-space()='{license}']]"
            f"//div[@role='cell'][{col_index}]//div"
        )

    def get_uploaded_file_name(self, file_name):
        locator = (By.XPATH,f"//div[contains(@class,'oxd-table-row')]//div[normalize-space()='{file_name}']//div")
        return self.selenium.get_text(locator)

    def get_work_experience_row_data(self, company_name) -> dict:
        from_text = self.selenium.get_text(
            self.get_cell_by_company_and_header(company_name, "From")
        )
        to_text = self.selenium.get_text(
            self.get_cell_by_company_and_header(company_name, "To")
        )
        return {
            "company": self.selenium.get_text(
                self.get_cell_by_company_and_header(company_name, "Company")
            ),
            "job_title": self.selenium.get_text(
                self.get_cell_by_company_and_header(company_name, "Job Title")
            ),
            "from_date": datetime.datetime.strptime(from_text, "%Y-%d-%m").date(),
            "to_date": datetime.datetime.strptime(to_text, "%Y-%d-%m").date(),
            "comment": self.selenium.get_text(
                self.get_cell_by_company_and_header(company_name, "Comment")
            ),
        }

    def fill_work_experience_from_and_save(self, work_experience):
        self.selenium.wait_till_visible(self.get_input_field_by_name("Company"))
        self.selenium.clear_and_type(self.get_input_field_by_name("Company"), work_experience.company)
        self.selenium.clear_and_type(self.get_input_field_by_name("Job Title"), work_experience.job_title)
        self.selenium.clear_and_type(self.get_input_field_by_name("From"), work_experience.from_date.strftime("%Y-%d-%m"))
        self.selenium.clear_and_type(self.get_input_field_by_name("To"), work_experience.to_date.strftime("%Y-%d-%m"))
        self.selenium.clear_and_type(self.comment_text_area, work_experience.comment)
        self.click_on_save_button()

    def fill_education_from_and_save(self, education):
        self.selenium.wait_till_visible(self.get_dropdown_label_by_name("Level"))
        self.selenium.wait_till_clickable(self.get_dropdown_label_by_name("Level")).click()

        """
        self.wait_for_loader_to_disappear()
        self.selenium.wait_till_visible(   #clickable
            self.get_random_dropdown_option_value(education.level)
        ).click()
        """

        education_level = self.selenium.wait_for_elements(self.get_all_dropdown_options())
        selected_option = random.choice(education_level)
        education.level = selected_option.text
        selected_option.click()
        self.selenium.clear_and_type(self.get_input_field_by_name("Institute"), education.institute)
        self.selenium.clear_and_type(self.get_input_field_by_name("Major/Specialization"), education.major_specialization)
        self.selenium.clear_and_type(self.get_input_field_by_name("Year"), education.year)
        self.selenium.clear_and_type(self.get_input_field_by_name("GPA/Score"), education.gpa_score)
        self.selenium.clear_and_type(self.get_input_field_by_name("Start Date"), education.start_date)
        self.selenium.clear_and_type(self.get_input_field_by_name("End Date"), education.end_date)
        self.click_on_save_button()

    def get_education_row_data(self, level_name) -> dict:
        return {
            "level": self.selenium.get_text(self.get_education_cell(level_name, 2)),
            "year": self.selenium.get_text(self.get_education_cell(level_name, 3)),
            "score": self.selenium.get_text(self.get_education_cell(level_name, 4))
        }

    def fill_skill_form_and_save(self, skill):
        self.selenium.wait_till_visible(self.get_dropdown_label_by_name("Skill"))
        self.selenium.wait_till_clickable(self.get_dropdown_label_by_name("Skill")).click()
        self.selenium.wait_till_clickable(self.get_random_dropdown_option_value(skill.skill)).click()  #clickable
        self.selenium.clear_and_type(self.get_input_field_by_name("Years of Experience"),skill.years_of_experience)
        self.selenium.clear_and_type(self.comment_text_area,skill.comments)
        self.click_on_save_button()

    def get_skill_row_data(self, skill) -> dict:
        return {
            "skill": self.selenium.get_text(
                self.get_skill_cell_by_index(skill, 2)
            ),
            "years": self.selenium.get_text(
                self.get_skill_cell_by_index(skill, 3)
            )
        }

    def fill_language_form_and_save(self) -> Language:
        language = Language()
        self.wait_for_loader_to_disappear()

        # -------- Language --------
        self.selenium.wait_till_clickable(
            self.get_dropdown_label_by_name("Language")
        ).click()

        language_options = self.selenium.wait_for_elements(
            self.get_all_dropdown_options()
        )
        selected_language = random.choice(language_options)
        language.language = selected_language.text
        selected_language.click()

        # -------- Fluency --------
        self.selenium.wait_till_clickable(
            self.get_dropdown_label_by_name("Fluency")
        ).click()

        fluency_options = self.selenium.wait_for_elements(
            self.get_all_dropdown_options()
        )
        selected_fluency = random.choice(fluency_options)
        language.fluency = selected_fluency.text
        selected_fluency.click()

        # -------- Competency --------
        self.selenium.wait_till_clickable(
            self.get_dropdown_label_by_name("Competency")
        ).click()

        competency_options = self.selenium.wait_for_elements(
            self.get_all_dropdown_options()
        )
        selected_competency = random.choice(competency_options)
        language.competency = selected_competency.text
        selected_competency.click()

        # -------- Save --------
        self.selenium.wait_till_visible(self.save_button)
        self.selenium.wait_till_clickable(
            self.save_button
        ).click()

        return language

    def get_language_row_data(self, language) -> dict:
        return {
            "language": self.selenium.get_text(
                self.get_language_cell_by_index(language, 2)
            ),
            "fluency": self.selenium.get_text(
                self.get_language_cell_by_index(language, 3)
            ),
            "competency": self.selenium.get_text(
                self.get_language_cell_by_index(language, 4)
            )
        }

    def fill_license_form_and_save(self, license: License) -> License:

        self.selenium.wait_till_clickable(self.get_dropdown_label_by_name("License Type")).click()

        license_type = self.selenium.wait_for_elements(self.get_all_dropdown_options())
        selected_license_type = random.choice(license_type)
        license.license_type = selected_license_type.text
        selected_license_type.click()

        self.selenium.clear_and_type(self.get_input_field_by_name("License Number"),license.license_number)
        self.selenium.clear_and_type(self.get_input_field_by_name("Issued Date"), license.issued_date)
        self.selenium.clear_and_type(self.get_input_field_by_name("Expiry Date"), license.expiry_date)
        self.selenium.wait_till_visible(self.save_button)
        self.selenium.wait_till_clickable(self.save_button).click()
        return license

    def get_license_row_data(self, license_type) -> dict:
        return {
            "license_type": self.selenium.get_text(
                self.get_license_cell_by_index(license_type,2)
            ),
            "issued_date": self.selenium.get_text(
                self.get_license_cell_by_index(license_type, 3)
            ),
            "expiry_date": self.selenium.get_text(
                self.get_license_cell_by_index(license_type,3)
            )
        }

    def upload_attachment(self, file_path):
        self.selenium.upload_file(self.attachment_input, file_path)
        self.selenium.wait_till_clickable(self.save_button).click()

    def click_on_add_button_by_name(self, form_name):
        self.selenium.wait_till_clickable(self.get_add_button_by_form_name(form_name)).click()

    def click_on_save_button(self):
        self.selenium.wait_till_clickable(self.save_button).click()

    def click_on_dropdown_label_by_name(self, label_name):
        self.selenium.wait_till_clickable(self.get_dropdown_label_by_name(label_name)).click()







