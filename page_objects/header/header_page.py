from selenium.webdriver.common.by import By
from page_objects.base.base_page import BasePage

class HeaderPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    user_profile_dropdown = (By.CSS_SELECTOR,"span.oxd-userdropdown-tab")

    def get_header_text_by_name(self, header_name):
        return (By.XPATH,f"//h6[normalize-space()='{header_name}']")

    def is_header_text_visible(self, header_name):
        return self.selenium.wait_till_visible(self.get_header_text_by_name_(header_name))

    def get_header_text_by_name_(self, page_name):
        return (By.XPATH,f"//h6[@class='oxd-text oxd-text--h6 oxd-topbar-header-breadcrumb-module'][text()='{page_name}']")

    def is_dashboard_text_visible(self):
        return self.selenium.wait_till_visible(self.get_header_text_by_name_("Dashboard"))

    def select_option_of_user_dropdown(self, dropdown_name):
        return (By.XPATH,f"//a[@class='oxd-userdropdown-link'][text()='{dropdown_name}']")

    def get_tab_from_nav_bar(self, tab_name):
        return (
            By.XPATH,
            f"//a[contains(@class,'oxd-topbar-body-nav-tab-item') and normalize-space()='{tab_name}']"
        )

    def click_on_tab_from_nav_bar(self, tab_name):
        self.wait_for_loader_to_disappear()
        self.selenium.wait_till_clickable(self.get_tab_from_nav_bar(tab_name)).click()

    def click_on_user_profile_dropdown_and_logout(self):
        self.selenium.wait_till_clickable(self.user_profile_dropdown).click()
        self.selenium.wait_till_clickable(self.select_option_of_user_dropdown("Logout")).click()