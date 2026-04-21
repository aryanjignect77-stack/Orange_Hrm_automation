import subprocess
import allure
import shutil
import os
import pytest

from data_factory.add_employee_data.add_employee_data import AddEmployeeData
from data_factory.admin.system_user_data import SystemUserData
from data_factory.login_data.login_data import LoginData
from page_objects.common.common_page import CommonPage
from page_objects.header.header_page import HeaderPage
from page_objects.left_side_menubar.left_side_menubar import LeftSideMenubar
from page_objects.login.login_page import LoginPage
from page_objects.pim.add_employee.add_employee_page import AddEmployeePage
from page_objects.pim.add_user.add_user_page import AddUserPage
from page_objects.pim.pim_page import PimPage
from utilities.browser_factory import BrowserFactory
from utilities.config_reader import ConfigReader
from utilities.logger import get_logger

LOG_DIR = "logs"
# Single source of truth — must match --alluredir in pytest CLI / CI command
ALLURE_RESULTS_DIR = "reports/allure-results"
ALLURE_REPORT_DIR = "reports/allure-report"


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default=ConfigReader.get_browser(),
        help="Browser to run tests on"
    )


@pytest.fixture(scope="session", autouse=True)
def global_test_setup(request):
    # Skip on xdist worker nodes — only the controller should do cleanup
    if hasattr(request.config, "workerinput"):
        return

    if os.path.exists(LOG_DIR):
        shutil.rmtree(LOG_DIR)
    os.makedirs(LOG_DIR, exist_ok=True)

    if os.path.exists(ALLURE_RESULTS_DIR):
        shutil.rmtree(ALLURE_RESULTS_DIR)
    os.makedirs(ALLURE_RESULTS_DIR, exist_ok=True)


@pytest.fixture(scope="function")
def driver(request):
    logger = get_logger()

    # Detect both Jenkins and GitHub Actions headless environments
    is_ci = os.getenv("JENKINS_HOME") is not None or os.getenv("CI") is not None

    browser_name = request.config.getoption("--browser")
    logger.info(f"Starting browser: {browser_name}")
    logger.info(f"Running in CI/headless mode: {is_ci}")

    driver = BrowserFactory.get_driver(browser_name, headless=is_ci)

    driver.implicitly_wait(30)
    driver.set_page_load_timeout(60)

    base_url = ConfigReader.get_base_url()
    logger.info(f"Navigating to {base_url}")
    driver.get(base_url)

    yield driver

    logger.info("Closing browser")
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot = driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name="Failure screenshot",
                attachment_type=allure.attachment_type.PNG
            )


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    # Skip on xdist worker nodes
    if hasattr(session.config, "workerinput"):
        return

    if os.path.exists(ALLURE_RESULTS_DIR):
        # FIX: shell=True + list only passes the first element to the shell on Linux.
        # Use a plain string so the shell receives the full command correctly.
        cmd = (
            f"allure generate {ALLURE_RESULTS_DIR} "
            f"-o {ALLURE_REPORT_DIR} --clean"
        )
        result = subprocess.run(cmd, shell=True)
        if result.returncode != 0:
            print(f"[WARN] Allure report generation failed (exit {result.returncode}). "
                  "Is 'allure' installed and on PATH?")


@pytest.fixture(scope="function")
def user_logged_in(driver):
    login_data = LoginData.get_valid_user_details()
    login_page = LoginPage(driver)
    login_page.enter_login_details(
        login_data["username"],
        login_data["password"]
    )
    return driver


@pytest.fixture(scope="function")
def create_employee_and_logout(driver):
    login_data = LoginData.get_valid_user_details()

    login_page = LoginPage(driver)
    left_side_menubar = LeftSideMenubar(driver)
    header_page = HeaderPage(driver)
    pim_page = PimPage(driver)
    add_employee_page = AddEmployeePage(driver)
    common_page = CommonPage(driver)

    login_page.enter_login_details(
        login_data["username"],
        login_data["password"]
    )

    employee = AddEmployeeData.get_valid_add_employee_details()

    left_side_menubar.click_menu_by_name("PIM")
    pim_page.click_on_button_by_name("Add")

    add_employee_page.fill_name_and_details(employee)
    add_employee_page.click_on_create_login_details_toggle_button()
    add_employee_page.fill_login_details(employee)
    add_employee_page.click_on_save_button()

    assert common_page.is_success_toast_message_displayed(), "Success toast message not displayed"

    header_page.click_on_user_profile_dropdown_and_logout()
    return employee


@pytest.fixture(scope="function")
def create_admin_system_user(driver, create_employee_and_logout):
    login_data = LoginData.get_valid_user_details()

    login_page = LoginPage(driver)
    left_side_menubar = LeftSideMenubar(driver)
    header_page = HeaderPage(driver)
    add_employee_page = AddEmployeePage(driver)
    add_user_page = AddUserPage(driver)
    common_page = CommonPage(driver)
    pim_page = PimPage(driver)

    login_page.enter_login_details(
        login_data["username"],
        login_data["password"]
    )

    employee = create_employee_and_logout
    employee_full_name = (
        f"{employee.first_name} "
        f"{employee.middle_name} "
        f"{employee.last_name}"
    )

    system_user = SystemUserData.get_system_user_details(employee_full_name)

    left_side_menubar.click_menu_by_name("Admin")
    assert header_page.get_header_text_by_name_("User Management")

    pim_page.click_on_button_by_name("Add")
    assert add_user_page.get_form_text_by_name("Add User")

    add_user_page.user_fills_in_all_mandatory_fields_and_clicks_save(system_user)
    add_employee_page.click_on_save_button()

    assert common_page.is_success_toast_message_displayed()

    header_page.click_on_user_profile_dropdown_and_logout()
    return system_user