from page_objects.header.header_page import HeaderPage
from data_factory.login_data.login_data import LoginData
from page_objects.login.login_page import LoginPage
from utilities.allure_helpers import log_step


def test_login_valid_user(driver):
    """
    Test login functionality with valid user credentials.
    Verifies that user can successfully log in to Orange HRM.
    """
    login_page = LoginPage(driver)
    login_data = LoginData.get_valid_user_details()
    login_invalid_data = LoginData.get_invalid_user_details()
    header_page = HeaderPage(driver)

    log_step("Navigating to the login page")
    assert login_page.get_header_text_by_name("Login"), "Login Page text not displayed"

    log_step("Login with invalid credentials")
    login_page.enter_login_details(login_invalid_data["username"], login_invalid_data["password"])
    assert login_page.is_invalid_credentials_text_displayed()

    log_step("Enter login details")
    login_page.enter_login_details(login_data["username"], login_data["password"])
    assert header_page.is_dashboard_text_visible(), "Dashboard text is not visible"

    log_step("User clicks on the Account Menu tab from navbar and clicks on Logout")
    header_page.click_on_user_profile_dropdown_and_logout()
    assert login_page.get_header_text_by_name("Login"), "Login Page text not displayed "


