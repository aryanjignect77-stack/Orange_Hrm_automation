from data_factory.recruitment_data.recruitment_data import RecruitmentData
from page_objects.common.common_page import CommonPage
from page_objects.header.header_page import HeaderPage
from page_objects.left_side_menubar.admin.admin_page import AdminPage
from page_objects.left_side_menubar.left_side_menubar import LeftSideMenubar
from page_objects.left_side_menubar.recruitment.recruitment_page import RecruitmentPage
from page_objects.pim.pim_page import PimPage
from page_objects.pim.qualifications.qualifications_page import QualificationsPage
from utilities.allure_helpers import log_step
from utilities.path_helpers import FilePaths


def test_verify_that_user_can_add_update_and_delete_candidate_from_recruitment_page(user_logged_in):

    left_side_menu = LeftSideMenubar(user_logged_in)
    common_page = CommonPage(user_logged_in)
    admin_page = AdminPage(user_logged_in)
    pim_page = PimPage(user_logged_in)
    recruitment_page = RecruitmentPage(user_logged_in)
    qualifications_page = QualificationsPage(user_logged_in)
    header_page = HeaderPage(user_logged_in)

    file_path = FilePaths.FILE_ATTACHMENT

    recruitment = RecruitmentData.get_recruitment_details()

    updated_candidate_data = RecruitmentData.get_recruitment_details()

    log_step("User navigates to the Recruitment page")
    left_side_menu.click_menu_by_name("Recruitment")
    assert common_page.is_form_displayed("Recruitment"), "Recruitment menu is not displayed"

    log_step("User clicks on the Add button from the candidates list table")
    pim_page.click_on_button_by_name("Add")
    assert common_page.is_form_displayed("Add Candidate"), "Add Candidate menu is not displayed"

    log_step("User fills in all mandatory fields and clicks on Save")
    qualifications_page.upload_attachment(file_path)
    recruitment_page.fill_candidate_details(recruitment)
    assert common_page.is_success_toast_message_displayed(), "Candidate not saved"

    log_step("User clicks on the Candidate tab from the navbar and navigates back to the candidates list page")
    header_page.click_on_tab_from_nav_bar("Candidates")
    assert common_page.is_form_header_text_displayed("Candidates"), "Candidates form is not displayed"

    log_step("User searches for the newly added candidate from the filter section")
    candidate_full_name = f"{recruitment.first_name} {recruitment.middle_name} {recruitment.last_name}"
    candidate_name = f"{recruitment.first_name}"
    admin_page.enter_search_value_for_system_user("Candidate Name", candidate_name)
    recruitment_page.select_candidate_from_autocomplete(candidate_full_name)
    pim_page.click_on_button_by_name("Search")
    assert recruitment_page.get_displayed_candidate_name(candidate_full_name) == candidate_full_name, \
        "Displayed candidate name does not match expected name"

    log_step("User clicks on the View icon for the newly added candidate from the candidates list table")
    recruitment_page.click_action_button_for_candidate(candidate_full_name, "view")
    assert common_page.is_form_displayed("Candidate Profile"), "Candidate Profile form is not displayed"
    assert recruitment_page.get_input_field_value_by_name("First Name") == recruitment.first_name
    assert recruitment_page.get_input_field_value_by_name("Middle Name") == recruitment.middle_name
    assert recruitment_page.get_input_field_value_by_name("Last Name") == recruitment.last_name

    log_step("User clicks on the Edit radio button from the Candidate Profile section")
    recruitment_page.click_edit_radio_button()
    assert pim_page.get_button_by_name("Save"), "Save button is not displayed"

    log_step("User updates the candidate’s details and clicks Save")
    recruitment_page.update_candidate_details(updated_candidate_data)
    recruitment_page.is_confirmation_pop_up_displayed()
    pim_page.click_on_button_by_name("Yes, Confirm")
    assert common_page.is_success_toast_message_displayed(), "Candidate not updated"
    assert recruitment_page.get_input_field_value_by_name("First Name") == updated_candidate_data.first_name
    assert recruitment_page.get_input_field_value_by_name("Middle Name") == updated_candidate_data.middle_name
    assert recruitment_page.get_input_field_value_by_name("Last Name") == updated_candidate_data.last_name

    log_step("User clicks on the Candidate tab from the navbar and navigates back to the candidates list page")
    header_page.click_on_tab_from_nav_bar("Candidates")
    assert common_page.is_form_header_text_displayed("Candidates"), "Candidates form is not displayed"

    log_step("User searches for the updated candidate from the filter section")
    updated_candidate_full_name = f"{updated_candidate_data.first_name} {updated_candidate_data.middle_name} {updated_candidate_data.last_name}"
    updated_candidate_name = f"{updated_candidate_data.first_name}"
    admin_page.enter_search_value_for_system_user("Candidate Name", updated_candidate_name)
    recruitment_page.select_candidate_from_autocomplete(updated_candidate_full_name)
    pim_page.click_on_button_by_name("Search")
    assert recruitment_page.get_displayed_candidate_name(updated_candidate_full_name) == updated_candidate_full_name, \
        "Displayed candidate name does not match expected name"

    log_step("User clicks on the Delete icon for the added candidate from the candidates list table")
    recruitment_page.click_action_button_for_candidate(updated_candidate_full_name, "delete")
    recruitment_page.is_confirmation_pop_up_displayed()
    pim_page.click_on_button_by_name("Yes, Delete")
    assert common_page.is_success_toast_message_displayed(), "Candidate not deleted"










