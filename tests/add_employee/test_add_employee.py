from data_factory.add_employee_data.add_employee_data import AddEmployeeData
from page_objects.header.header_page import HeaderPage
from page_objects.left_side_menubar.left_side_menubar import LeftSideMenubar
from page_objects.login.login_page import LoginPage
from page_objects.pim.add_employee.add_employee_page import AddEmployeePage
from page_objects.pim.employee_list.employee_list_page import EmployeeListPage
from page_objects.pim.pim_page import PimPage
from utilities.allure_helpers import log_step
from page_objects.common.common_page import CommonPage


def test_verify_that_a_newly_added_employee_appears_in_the_employee_list_and_does_not_have_admin_access_upon_login(user_logged_in):

    left_side_menubar = LeftSideMenubar(user_logged_in)
    header_page = HeaderPage(user_logged_in)
    pim_page = PimPage(user_logged_in)
    add_employee_page = AddEmployeePage(user_logged_in)
    employee_list_page = EmployeeListPage(user_logged_in)
    login_page = LoginPage(user_logged_in)
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

    log_step("User clicks on the Employee List tab from the navbar")
    assert pim_page.is_personal_details_text_visible(), "personal details text not visible"
    header_page.click_on_tab_from_nav_bar("Employee List")
    assert pim_page.is_header_text_visible("Employee Information"), "Employee Information Page text not displayed"

    log_step("User searches for the newly created Employee from the filter section")
    employee_list_page.enter_text_in_text_box_by_label("Employee Name", employee.first_name + " " + employee.last_name)
    pim_page.click_on_button_by_name("Search")
    search_result_id = pim_page.get_employee_id_from_search_result(employee.employee_id)
    assert search_result_id == employee.employee_id, "employee id mismatch"

    log_step("User clicks on the Account Menu tab from navbar and clicks on Logout")
    header_page.click_on_user_profile_dropdown_and_logout()
    assert login_page.get_header_text_by_name("Login"), "Login Page text not displayed"

    log_step("User logs in using the newly created employee’s credentials")
    login_page.enter_login_details(employee.username, employee.password)
    assert header_page.is_dashboard_text_visible(), "Dashboard text not displayed"
    assert not left_side_menubar.is_menu_displayed("PIM"), "Admin menu is displayed"







