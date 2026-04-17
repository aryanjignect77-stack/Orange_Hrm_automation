import os

from data_factory.edit_info.edit_info_data import EditInfoData
from data_factory.qualifications_data.education_data.education_data import EducationData
from data_factory.qualifications_data.license_data.license_data import LicenseData
from data_factory.qualifications_data.skill_data.skill_data import SkillData
from data_factory.qualifications_data.work_experience_data.work_experience_data import WorkExperienceData
from page_objects.common.common_page import CommonPage
from page_objects.left_side_menubar.left_side_menubar import LeftSideMenubar
from page_objects.left_side_menubar.my_info.personal_details.personal_details import PersonalDetails
from page_objects.login.login_page import LoginPage
from page_objects.pim.add_employee.add_employee_page import AddEmployeePage
from page_objects.pim.pim_page import PimPage
from page_objects.pim.qualifications.qualifications_page import QualificationsPage
from utilities.allure_helpers import log_step
from utilities.path_helpers import FilePaths


def test_verify_that_personal_details_can_be_updated_on_the_my_info_page_and_changes_are_saved_correctly(user_logged_in):

    left_side_menu = LeftSideMenubar(user_logged_in)
    pim_page = PimPage(user_logged_in)
    personal_details_page = PersonalDetails(user_logged_in)
    common_page = CommonPage(user_logged_in)

    edit_info = EditInfoData.get_my_info_details()

    log_step("User navigates to the My Info page")
    left_side_menu.click_menu_by_name("My Info")
    assert pim_page.is_personal_details_text_visible(), "Personal details page not displayed"

    log_step("User Updates the personal details and clicks on the Save button")
    personal_details_page.enter_text_in_field(edit_info)
    personal_details_page.select_random_dropdown_value("Nationality")
    personal_details_page.select_random_dropdown_value("Marital Status")
    personal_details_page.click_on_save_button()
    # assert add_employee_page.is_success_toast_displayed(), "Success message not displayed"
    assert common_page.is_success_toast_message_displayed(), "Success toast message not displayed"

    log_step("Verify personal have updated data")
    updated_details = personal_details_page.get_updated_personal_details()

    assert updated_details["firstName"] == edit_info.first_name
    assert updated_details["middleName"] == edit_info.middle_name
    assert updated_details["lastName"] == edit_info.last_name
    assert updated_details["Other Id"] == edit_info.other_id

def test_verify_that_users_can_add_or_update_their_profile_picture_in_the_my_info_section(user_logged_in):

    left_side_menu = LeftSideMenubar(user_logged_in)
    personal_details_page = PersonalDetails(user_logged_in)
    pim_page = PimPage(user_logged_in)
    common_page = CommonPage(user_logged_in)

    image_path = FilePaths.PROFILE_PICTURE

    log_step("User navigates to the My Info page")
    left_side_menu.click_menu_by_name("My Info")
    assert pim_page.is_personal_details_text_visible(), "Personal details text not displayed"

    log_step("User clicks on the profile picture")
    personal_details_page.click_on_profile_picture()
    assert personal_details_page.get_form_title_by_name("Change Profile Picture"), "Change profile picture page is not displayed"

    log_step("User changes the profile picture from the Change Profile Picture section and clicks on the Save button")
    personal_details_page.upload_image(image_path)
    assert common_page.is_success_toast_message_displayed(), "Success toast message not displayed \ Profile picture not updated"

def test_verify_that_qualifications_can_be_added_in_the_my_info_section_and_are_displayed_correctly(driver, create_employee_and_logout):
    employee = create_employee_and_logout

    left_side_menu = LeftSideMenubar(driver)
    pim_page = PimPage(driver)
    common_page = CommonPage(driver)
    qualifications_page = QualificationsPage(driver)

    work_experience = WorkExperienceData.get_work_experience_details()
    education = EducationData.get_education_details()
    skill = SkillData.get_skill_details()
    license = LicenseData.get_license_details()

    file_path = FilePaths.FILE_ATTACHMENT

    login_page = LoginPage(driver)
    login_page.enter_login_details(employee.username, employee.password)

    log_step("User navigates to the My Info page")
    left_side_menu.click_menu_by_name("My Info")
    assert pim_page.is_personal_details_text_visible(), "Personal details text not displayed"

    log_step("User clicks on the qualifications tab from the User Details section's sidebar")
    pim_page.click_on_tab_by_name("Qualifications")
    assert common_page.get_form_header_text("Qualifications"), "Qualifications page is not displayed"

    log_step("User clicks on the Add button from the Work Experience section")
    qualifications_page.click_on_add_button_by_name("Work Experience")
    assert common_page.get_form_header_text("Add Work Experience"), "Add Work Experience form not displayed"

    log_step("User fills in all mandatory fields and clicks Save")
    qualifications_page.fill_work_experience_from_and_save(work_experience)
    assert common_page.is_success_toast_message_displayed(), "Work experience not saved"
    actual_data = qualifications_page.get_work_experience_row_data(
        work_experience.company
    )
    assert actual_data["company"] == work_experience.company
    assert actual_data["job_title"] == work_experience.job_title
    assert actual_data["from_date"] == work_experience.from_date
    assert actual_data["to_date"] == work_experience.to_date
    assert actual_data["comment"] == work_experience.comment

    log_step("User clicks on the Add button from the Education section")
    qualifications_page.click_on_add_button_by_name("Education")
    assert common_page.get_form_header_text("Add Education"), "Add Education form not displayed"

    log_step("User fills in all mandatory fields and clicks Save")
    qualifications_page.fill_education_from_and_save(education)
    assert common_page.is_success_toast_message_displayed(), "Education not saved"
    actual_data = qualifications_page.get_education_row_data(education.level)
    assert actual_data["level"] == education.level
    assert actual_data["year"] == education.year
    assert actual_data["score"] == education.gpa_score

    log_step("User clicks on the Add button from the Skills section")
    qualifications_page.click_on_add_button_by_name("Skills")
    assert common_page.get_form_header_text("Add Skill"), "Add Skill form not displayed"

    log_step("User fills in all mandatory fields and clicks Save")
    qualifications_page.fill_skill_form_and_save(skill)
    assert common_page.is_success_toast_message_displayed(), "Skill not saved"
    actual_skill = qualifications_page.get_skill_row_data(skill.skill)
    assert actual_skill["skill"] == skill.skill
    assert actual_skill["years"] == skill.years_of_experience

    log_step("User clicks on the Add button from the Languages section")
    qualifications_page.click_on_add_button_by_name("Languages")
    assert common_page.get_form_header_text("Add Language"), "Add Language form not displayed"

    log_step("User fills in all mandatory fields and clicks Save")
    actual_language = qualifications_page.fill_language_form_and_save()
    assert common_page.is_success_toast_message_displayed(), "Language not saved"
    row_data = qualifications_page.get_language_row_data(
        actual_language.language
    )
    assert row_data["language"] == actual_language.language
    assert row_data["fluency"] == actual_language.fluency
    assert row_data["competency"] == actual_language.competency

    log_step("User clicks on the Add button from the License section")
    qualifications_page.click_on_add_button_by_name("License")
    assert common_page.get_form_header_text("Add License"), "Add License form not displayed"

    log_step("User fills in all mandatory fields and clicks Save")
    qualifications_page.fill_license_form_and_save(license)
    assert common_page.is_success_toast_message_displayed(), "License Data not saved"

    actual_license = qualifications_page.get_license_row_data(license.license_type)
    assert actual_license["license_type"] == license.license_type
    assert actual_license["issued_date"] == license.issued_date
    assert actual_license["expiry_date"] == license.issued_date

    log_step("User clicks on the Add button from the Attachments section")
    qualifications_page.click_on_add_button_by_name("Attachments")
    assert common_page.get_form_header_text("Add Attachment"), "Add Attachment form not displayed"

    log_step("User fills in all mandatory fields and clicks Save")
    expected_file_name = os.path.basename(file_path)
    qualifications_page.upload_attachment(file_path)
    assert common_page.is_success_toast_message_displayed(), "Attachment not saved"
    actual_file_name = qualifications_page.get_uploaded_file_name(expected_file_name)
    assert actual_file_name == expected_file_name
































