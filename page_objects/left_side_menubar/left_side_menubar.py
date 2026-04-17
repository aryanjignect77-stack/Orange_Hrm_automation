from selenium.webdriver.common.by import By
from page_objects.base.base_page import BasePage

class LeftSideMenubar(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def search_menu_by_name(self, menu_name):
        return (By.XPATH,f"//span[@class='oxd-text oxd-text--span oxd-main-menu-item--name'][text()='{menu_name}']")

    def click_menu_by_name(self, menu_name):
        self.wait_for_loader_to_disappear()
        self.selenium.wait_till_clickable(self.search_menu_by_name(menu_name)).click()

    def is_menu_displayed(self, menu_name):
        return self.selenium.is_element_displayed(self.search_menu_by_name(menu_name))