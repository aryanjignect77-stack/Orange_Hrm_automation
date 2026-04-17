from data_factory.add_employee_data.add_employee_data import AddEmployeeData
from data_factory.admin.system_user_data import SystemUserData
from data_factory.edit_job_details.edit_job_details_data import EditJobDetailsData
from data_factory.login_data.login_data import LoginData
from page_objects.common.common_page import CommonPage
from page_objects.header.header_page import HeaderPage
from page_objects.left_side_menubar.admin.admin_page import AdminPage
from page_objects.left_side_menubar.left_side_menubar import LeftSideMenubar
from page_objects.login.login_page import LoginPage
from page_objects.pim.add_employee.add_employee_page import AddEmployeePage
from page_objects.pim.add_user.add_user_page import AddUserPage
from page_objects.pim.employee_list.employee_list_page import EmployeeListPage
from page_objects.pim.pim_page import PimPage
from utilities.allure_helpers import log_step


def test_verify_that_a_new_system_user_can_be_created_in_admin_and_can_log_in_with_the_assigned_credentials(user_logged_in):

    login_page = LoginPage(user_logged_in)
    left_side_menu_page = LeftSideMenubar(user_logged_in)
    header_page = HeaderPage(user_logged_in)
    pim_page = PimPage(user_logged_in)
    add_user_page = AddUserPage(user_logged_in)
    add_employee_page = AddEmployeePage(user_logged_in)
    left_side_menubar = LeftSideMenubar(user_logged_in)
    admin_page = AdminPage(user_logged_in)
    common_page = CommonPage(user_logged_in)

    employee = AddEmployeeData.get_valid_add_employee_details()

    log_step("User navigates to the PIM page")
    left_side_menubar.click_menu_by_name("PIM")
    assert header_page.get_header_text_by_name_("PIM"), "PIM Page text not displayed"

    log_step("User clicks the Add button in the employee list table")
    pim_page.click_on_button_by_name("Add")
    assert add_employee_page.is_add_employee_text_displayed(), "Add Employee Page text not displayed"

    log_step("User fills in all mandatory fields including login details and clicks Save button")
    add_employee_page.fill_name_and_details(employee)
    add_employee_page.click_on_create_login_details_toggle_button()
    add_employee_page.fill_login_details(employee)
    add_employee_page.click_on_save_button()
    # assert add_employee_page.is_success_toast_displayed(), "Success toast message not displayed"
    assert common_page.is_success_toast_message_displayed(), "Success toast message not displayed"

    log_step("User navigates to the Admin → User Management page")
    left_side_menu_page.click_menu_by_name("Admin")
    assert header_page.get_header_text_by_name_("User Management"), "User Management text is not displayed"

    log_step("User clicks on the Add button from the system user list table")
    pim_page.click_on_button_by_name("Add")
    assert add_user_page.get_form_text_by_name("Add User"), "Add User from text not displayed"

    log_step("User fills in all mandatory fields and clicks Save")
    employee_full_name = f"{employee.first_name} {employee.middle_name} {employee.last_name}"
    system_user = SystemUserData.get_system_user_details(employee_full_name)
    add_user_page.user_fills_in_all_mandatory_fields_and_clicks_save(
        system_user
    )
    add_employee_page.click_on_save_button()
    # assert add_employee_page.is_success_toast_displayed(), "Success toast message not displayed"
    assert common_page.is_success_toast_message_displayed(), "Success toast message not displayed"
    assert header_page.get_header_text_by_name_("User Management"), "User Management text is not displayed"

    log_step("User searches for the newly created System User from the filter section")
    admin_page.enter_search_value_for_system_user("Username",system_user.username)
    pim_page.click_on_button_by_name("Search")
    assert admin_page.get_employee_search_result_text(system_user.username) == system_user.username, "Employee not found"

    log_step("User clicks on the Account Menu tab from navbar and clicks on Logout")
    header_page.click_on_user_profile_dropdown_and_logout()
    assert login_page.get_header_text_by_name("Login"), "Login Page text not displayed"

    log_step("User logs in using the newly created system user’s credentials")
    login_page.enter_login_details(system_user.username, system_user.password)
    assert left_side_menu_page.is_menu_displayed("Admin"), "Admin menu is not displayed"

def test_verify_that_admin_can_update_job_details_of_an_employee_and_updated_information_is_visible_after_login(driver, create_employee_and_logout):
    employee = create_employee_and_logout

    login_page = LoginPage(driver)
    pim_page = PimPage(driver)
    common_page = CommonPage(driver)
    left_side_menu = LeftSideMenubar(driver)
    employee_list_page = EmployeeListPage(driver)
    header_page = HeaderPage(driver)


    edit_job_details = EditJobDetailsData.get_job_details()

    login_data = LoginData.get_valid_user_details()

    log_step("User login with valid credentials")
    login_page.enter_login_details(login_data["username"], login_data["password"])
    assert (
            common_page.is_form_displayed("Dashboard")
            or pim_page.is_personal_details_text_visible()
    ), "Neither Dashboard nor Personal Details page is displayed after login"

    log_step("Admin navigates to the PIM page")
    left_side_menu.click_menu_by_name("PIM")
    assert common_page.is_form_displayed("PIM"), "PIM page is not displayed"

    log_step("Admin searches for the employee")
    expected_display_name = " ".join(
        filter(None, [employee.first_name, employee.middle_name])
    )
    pim_page.search_employee_by_name("Employee Name",expected_display_name)
    pim_page.click_on_button_by_name("Search")
    actual_name = pim_page.get_employee_name_from_search_result(
        expected_display_name
    )
    assert actual_name == expected_display_name

    log_step("Admin clicks the edit icon for the employee in the employee list table")
    pim_page.click_on_edit_icon_button()
    assert pim_page.is_personal_details_text_visible(), "Personal details text not displayed"

    log_step("Admin clicks on the Job tab from the User Details section's sidebar")
    employee_list_page.click_on_tab_by_name("Job")
    assert common_page.get_form_header_text("Job Details"), "Job Details page is not displayed"

    log_step("Admin updates the job details and clicks on the save button")
    employee_list_page.update_job_details_and_click_on_save_button(edit_job_details)
    assert common_page.is_success_toast_message_displayed(), "Job details not updated"

    log_step("Admin logs out of the application")
    header_page.click_on_user_profile_dropdown_and_logout()
    assert login_page.get_header_text_by_name("Login"), "Login Page not displayed"

    log_step("Log in with the credentials of the employee for which the job details were updated")
    login_page.enter_login_details(employee.username, employee.password)
    assert common_page.get_form_header_text("Dashboard"), "Dashboard page is not displayed"

    log_step("Employee navigates to the My Info page")
    left_side_menu.click_menu_by_name("My Info")
    assert common_page.get_form_header_text("PIM"), "My Info page is not displayed"

    log_step("Employee clicks on the Job tab from the User Details section's sidebar")
    pim_page.click_on_tab_by_name("Job")
    assert common_page.get_form_header_text("Job Details"), "Job Details Form is not displayed"

    assert employee_list_page.get_selected_dropdown_value_by_label("Job Title") == edit_job_details.job_title
    assert employee_list_page.get_selected_dropdown_value_by_label("Job Category") == edit_job_details.job_category
    assert employee_list_page.get_selected_dropdown_value_by_label("Sub Unit") == edit_job_details.sub_unit
    assert employee_list_page.get_selected_dropdown_value_by_label("Location") == edit_job_details.location
    assert employee_list_page.get_selected_dropdown_value_by_label(
        "Employment Status") == edit_job_details.employment_status

    assert employee_list_page.get_date_value_by_label("Joined Date") == edit_job_details.joined_date

def test_verify_that_sorting_functionality_works_for_all_columns_in_admin_user_management_table(user_logged_in):

    left_side_menu = LeftSideMenubar(user_logged_in)
    common_page = CommonPage(user_logged_in)
    admin_page = AdminPage(user_logged_in)

    log_step("User navigates to the Admin → User Management page")
    left_side_menu.click_menu_by_name("Admin")
    assert common_page.get_form_header_text("User Management")

    log_step("Sort Username column in Descending order")
    admin_page.sort_column("Username", "Descending")
    usernames_desc = admin_page.get_column_values("Username")
    admin_page.assert_column_sorted(usernames_desc, "Descending")

    log_step("Sort Username column in Ascending order")
    admin_page.sort_column("Username", "Ascending")
    usernames_asc = admin_page.get_column_values("Username")
    admin_page.assert_column_sorted(usernames_asc, "Ascending")

    log_step("Sort the User Role column in descending order")
    admin_page.sort_column("User Role", "Descending")
    user_role_desc = admin_page.get_column_values("User Role")
    admin_page.assert_column_sorted(user_role_desc,"Descending")

    log_step("Sort the User Role column in ascending order")
    admin_page.sort_column("User Role","Ascending")
    user_role_asc = admin_page.get_column_values("User Role")
    admin_page.assert_column_sorted(user_role_asc,"Ascending")

    log_step("Sort the Employee Name column in descending order")
    admin_page.sort_column("Employee Name", "Descending")
    employee_name_desc = admin_page.get_column_values("Employee Name")
    admin_page.assert_column_sorted(employee_name_desc,"Descending")

    log_step("Sort the Employee Name column in ascending order")
    admin_page.sort_column("Employee Name","Ascending")
    employee_name_asc = admin_page.get_column_values("Employee Name")
    admin_page.assert_column_sorted(employee_name_asc,"Ascending")

    log_step("Sort the Status column in descending order")
    admin_page.sort_column("Status", "Descending")
    status_desc = admin_page.get_column_values("Status")
    admin_page.assert_column_sorted(status_desc,"Descending")

    log_step("Sort the Status column in ascending order")
    admin_page.sort_column("Status","Ascending")
    status_asc = admin_page.get_column_values("Status")
    admin_page.assert_column_sorted(status_asc,"Ascending")

def test_verify_that_search_functionality_filters_results_correctly_on_admin_user_management_page(driver,create_admin_system_user):

    login_page = LoginPage(driver)
    left_side_menu = LeftSideMenubar(driver)
    common_page = CommonPage(driver)
    admin_page = AdminPage(driver)
    pim_page = PimPage(driver)

    system_user = create_admin_system_user

    log_step("User enter system user credentials")
    login_page.enter_login_details(system_user.username, system_user.password)
    assert common_page.get_form_header_text("Dashboard"), "Dashboard Page is not visible"

    log_step("User navigates to the Admin → User Management page")
    left_side_menu.click_menu_by_name("Admin")
    assert common_page.get_form_header_text("User Management"), "User Management Page is not displayed"

    log_step("Search for a system user using the Username")
    admin_page.enter_search_value_for_system_user("Username", system_user.username)
    pim_page.click_on_button_by_name("Search")
    assert admin_page.get_employee_search_result_text(
        system_user.username) == system_user.username, "System User not found"
    pim_page.click_on_button_by_name("Reset")

    log_step("Search for a system user using the User Role")
    admin_page.get_dropdown_by_label("User Role")
    admin_page.click_on_option("Admin")
    pim_page.click_on_button_by_name("Search")
    assert admin_page.get_employee_search_result_text(
        system_user.username) == system_user.username, "System User not found"
    pim_page.click_on_button_by_name("Reset")

    log_step("Search for a system user using the Employee Name")
    admin_page.enter_search_value_for_system_user("Employee Name", system_user.employee_name)
    admin_page.get_dropdown_option_for_employee_name(system_user.employee_name)
    pim_page.click_on_button_by_name("Search")
    assert admin_page.is_user_present_with_username_and_role(
        system_user.username,
        "Admin"
    ), "System user found but role is not Admin"
    pim_page.click_on_button_by_name("Reset")

    log_step("Search for a system user using the Status")
    admin_page.get_dropdown_by_label("Status")
    admin_page.click_on_option("Enabled")
    pim_page.click_on_button_by_name("Search")
    assert admin_page.get_employee_search_result_text(
        system_user.username) == system_user.username, "System user not found"
    pim_page.click_on_button_by_name("Reset")

    log_step("Search for a system user using all filter attribute")
    admin_page.enter_search_value_for_system_user("Username", system_user.username)
    admin_page.get_dropdown_by_label("User Role")
    admin_page.click_on_option("Admin")
    admin_page.enter_search_value_for_system_user("Employee Name", system_user.employee_name)
    admin_page.get_dropdown_option_for_employee_name(system_user.employee_name)
    admin_page.get_dropdown_by_label("Status")
    admin_page.click_on_option("Enabled")
    pim_page.click_on_button_by_name("Search")
    assert admin_page.get_user_table_cell_value_by_username(
        system_user.username, 2
    ) == system_user.username, "User name mismatch"

    assert admin_page.get_user_table_cell_value_by_username(
        system_user.username, 3
    ) == "Admin", "User role mismatch"

    actual_employee_name = admin_page.get_user_table_cell_value_by_username(
        system_user.username, 4
    )
    parts = system_user.employee_name.split()
    expected_first_last = f"{parts[0]} {parts[-1]}"
    assert actual_employee_name == expected_first_last, \
        "Employee name mismatch"

    assert admin_page.get_user_table_cell_value_by_username(
        system_user.username, 5
    ) == "Enabled", "User status mismatch"

    log_step("Reset the search filter")
    pim_page.click_on_button_by_name("Reset")
    assert admin_page.get_search_input_value("Username") == "", \
        "Username field is not cleared"

    assert admin_page.get_search_input_value("Employee Name") == "", \
        "Employee Name field is not cleared"

    assert admin_page.get_dropdown_selected_value_by_label("User Role") == "-- Select --", \
        "User Role dropdown not reset"

    assert admin_page.get_dropdown_selected_value_by_label("Status") == "-- Select --", \
        "Status dropdown not reset"

























































